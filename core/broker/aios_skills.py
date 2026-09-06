#!/usr/bin/env python3
"""Personal AI OS v0.1 registry, broker, maintenance, and validation CLI."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
AIOS_ROOT = REPOSITORY_ROOT / "core"
DEFAULT_REGISTRY = AIOS_ROOT / "registry" / "skill-registry.json"
DEFAULT_SCHEMA = AIOS_ROOT / "registry" / "skill-registry.schema.json"
OFFICIAL_VALIDATOR = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"

TRUST_RANK = {
    "AUTHORITATIVE": 4,
    "VERIFIED": 3,
    "COMMUNITY": 2,
    "EXPERIMENTAL": 1,
    "DISABLED": 0,
}
ACTIVATION_RANK = {"LOW": 2, "MEDIUM": 1, "HIGH": 0}
REQUIRED_ENTRY_FIELDS = {
    "id", "name", "description", "category", "capabilities", "triggers",
    "location", "scope", "publisher", "source", "version", "license",
    "trust_level", "status", "enabled", "installed", "dependencies",
    "conflicts", "recommended_agents", "activation_cost", "compatibility",
    "quality", "notes", "last_validated",
}
TRUST_LEVELS = set(TRUST_RANK)
STATUSES = {"AVAILABLE", "UNAVAILABLE", "DISABLED"}
SCOPES = {"shared", "private", "external"}
BROAD_TRIGGERS = {"help", "analysis", "task", "project", "work", "research"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"registry file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def save_registry_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def normalize_words(value: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", value.lower().replace("optimisation", "optimization"))
    normalized: set[str] = set()
    for word in words:
        if len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        normalized.add(word)
    return normalized


def is_selectable(entry: dict[str, Any], entries_by_id: dict[str, dict[str, Any]]) -> tuple[bool, str | None]:
    if not entry.get("enabled") or entry.get("status") != "AVAILABLE" or entry.get("trust_level") == "DISABLED":
        return False, "disabled or unavailable"
    if not entry.get("installed"):
        return False, "not installed"
    location = Path(entry.get("location", ""))
    if entry.get("scope") != "external" and not location.exists():
        return False, "registered location is unavailable"
    for dependency in entry.get("dependencies", []):
        if dependency.get("optional"):
            continue
        target = entries_by_id.get(dependency.get("id"))
        if not target:
            return False, f"required dependency missing: {dependency.get('id')}"
        allowed, reason = is_selectable_shallow(target)
        if not allowed:
            return False, f"required dependency unusable: {dependency.get('id')} ({reason})"
    return True, None


def is_selectable_shallow(entry: dict[str, Any]) -> tuple[bool, str | None]:
    if not entry.get("enabled") or entry.get("status") != "AVAILABLE" or entry.get("trust_level") == "DISABLED":
        return False, "disabled or unavailable"
    if not entry.get("installed"):
        return False, "not installed"
    return True, None


def candidate_rank(entry: dict[str, Any], relevance: float) -> tuple[float, int, int, str]:
    return (
        relevance,
        TRUST_RANK.get(entry.get("trust_level", "DISABLED"), 0),
        ACTIVATION_RANK.get(entry.get("activation_cost", "HIGH"), 0),
        entry.get("id", ""),
    )


def capability_candidates(data: dict[str, Any], capability: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    entries = data.get("skills", [])
    by_id = {entry.get("id"): entry for entry in entries}
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    for entry in entries:
        if capability not in entry.get("capabilities", []):
            continue
        usable, reason = is_selectable(entry, by_id)
        if usable:
            accepted.append(entry)
        else:
            rejected.append({"id": entry.get("id", "unknown"), "reason": reason or "unusable"})
    accepted.sort(key=lambda entry: candidate_rank(entry, 1.0), reverse=True)
    return accepted, rejected


def infer_task_candidates(data: dict[str, Any], task: str) -> list[tuple[dict[str, Any], float, list[str]]]:
    task_words = normalize_words(task)
    entries = data.get("skills", [])
    by_id = {entry.get("id"): entry for entry in entries}
    results: list[tuple[dict[str, Any], float, list[str]]] = []
    for entry in entries:
        if entry.get("id") == "skill-broker":
            continue
        usable, _ = is_selectable(entry, by_id)
        if not usable:
            continue
        matched: list[str] = []
        score = 0.0
        for phrase in entry.get("triggers", []):
            words = normalize_words(phrase)
            if not words:
                continue
            overlap = len(words & task_words) / len(words)
            if overlap >= 0.66 and len(words & task_words) >= 2:
                matched.append(phrase)
                score = max(score, 3.0 + overlap)
        for capability in entry.get("capabilities", []):
            words = normalize_words(capability)
            overlap_count = len(words & task_words)
            if words and overlap_count >= 2:
                matched.append(capability)
                score = max(score, 2.0 + overlap_count / len(words))
        if score > 0:
            results.append((entry, score, sorted(set(matched))))
    results.sort(key=lambda item: candidate_rank(item[0], item[1]), reverse=True)
    return results


def broker(data: dict[str, Any], task: str | None, capabilities: list[str]) -> dict[str, Any]:
    selected: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []
    missing: list[str] = []
    required: list[str] = list(dict.fromkeys(capabilities))
    selected_ids: set[str] = set()

    for capability in required:
        candidates, unusable = capability_candidates(data, capability)
        rejected.extend(unusable)
        if not candidates:
            missing.append(capability)
            continue
        winner = candidates[0]
        if winner["id"] not in selected_ids:
            selected.append({"id": winner["id"], "reason": f"best trusted compatible match for {capability}"})
            selected_ids.add(winner["id"])
        for candidate in candidates[1:]:
            rejected.append({"id": candidate["id"], "reason": f"redundant for {capability}; stronger equivalent selected"})

    # Explicit capability requirements are authoritative. Use semantic task
    # inference only when the caller has not already supplied a bounded set;
    # otherwise broad task words can activate unrelated adjacent skills.
    if task and not required:
        task_results = infer_task_candidates(data, task)
        task_words = normalize_words(task)
        for entry, _, matches in task_results:
            if entry["id"] not in selected_ids:
                selected.append({"id": entry["id"], "reason": "task signals: " + ", ".join(matches)})
                selected_ids.add(entry["id"])
            capabilities_for_entry = entry.get("capabilities", [])
            if capabilities_for_entry:
                inferred_capability = max(
                    capabilities_for_entry,
                    key=lambda capability: (len(normalize_words(capability) & task_words), -capabilities_for_entry.index(capability)),
                )
                required.append(inferred_capability)

    return {
        "task": task,
        "required_capabilities": list(dict.fromkeys(required)),
        "selected": selected,
        "rejected": rejected,
        "missing_capabilities": missing,
    }


def parse_frontmatter(skill_file: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"cannot read {skill_file}: {exc}"]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{skill_file}: missing YAML frontmatter start"]
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{skill_file}: missing YAML frontmatter end"]
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, errors


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def duplicate_report(data: dict[str, Any]) -> dict[str, dict[str, list[str]] | list[str]]:
    entries = data.get("skills", [])
    id_counts = Counter(entry.get("id") for entry in entries)
    duplicate_ids = sorted(str(key) for key, count in id_counts.items() if key and count > 1)
    capability_owners: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        for capability in entry.get("capabilities", []):
            capability_owners[capability].append(entry.get("id", "unknown"))
    overlaps = {key: sorted(set(value)) for key, value in capability_owners.items() if len(set(value)) > 1}
    internal: dict[str, list[str]] = {}
    for entry in entries:
        counts = Counter(entry.get("capabilities", []))
        duplicates = sorted(key for key, count in counts.items() if count > 1)
        if duplicates:
            internal[entry.get("id", "unknown")] = duplicates
    return {"duplicate_ids": duplicate_ids, "cross_skill_capability_overlaps": overlaps, "duplicate_capabilities_within_entry": internal}


def validate_registry(data: dict[str, Any], registry_path: Path, run_official: bool = True) -> dict[str, list[str] | bool]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("registry_version", ""))):
        errors.append("registry_version must use semantic versioning")
    entries = data.get("skills")
    if not isinstance(entries, list):
        return {"passed": False, "errors": errors + ["skills must be an array"], "warnings": warnings}

    duplicates = duplicate_report(data)
    for duplicate_id in duplicates["duplicate_ids"]:
        errors.append(f"duplicate skill id: {duplicate_id}")
    for owner, capabilities in duplicates["duplicate_capabilities_within_entry"].items():
        errors.append(f"duplicate capabilities within {owner}: {', '.join(capabilities)}")
    for capability, owners in duplicates["cross_skill_capability_overlaps"].items():
        warnings.append(f"overlapping capability {capability}: {', '.join(owners)}")

    by_id = {entry.get("id"): entry for entry in entries if isinstance(entry, dict)}
    for index, entry in enumerate(entries):
        label = entry.get("id", f"index-{index}") if isinstance(entry, dict) else f"index-{index}"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        missing_fields = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        if missing_fields:
            errors.append(f"{label}: missing fields: {', '.join(missing_fields)}")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
            errors.append(f"{label}: invalid id")
        if len(entry["description"].strip()) < 20:
            errors.append(f"{label}: description is missing or too short")
        if entry["trust_level"] not in TRUST_LEVELS:
            errors.append(f"{label}: invalid trust level {entry['trust_level']}")
        if entry["status"] not in STATUSES:
            errors.append(f"{label}: invalid status {entry['status']}")
        if entry["scope"] not in SCOPES:
            errors.append(f"{label}: invalid scope {entry['scope']}")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", entry["version"]):
            errors.append(f"{label}: invalid semantic version {entry['version']}")
        if not isinstance(entry["capabilities"], list) or not entry["capabilities"]:
            errors.append(f"{label}: capabilities must be a non-empty array")
        if not isinstance(entry["triggers"], list) or not entry["triggers"]:
            errors.append(f"{label}: triggers must be a non-empty array")
        for trigger in entry.get("triggers", []):
            if trigger.strip().lower() in BROAD_TRIGGERS or len(normalize_words(trigger)) < 2:
                errors.append(f"{label}: trigger is overly broad: {trigger}")
        if entry["trust_level"] == "DISABLED" and (entry["enabled"] or entry["status"] != "DISABLED"):
            errors.append(f"{label}: DISABLED trust must have enabled=false and status=DISABLED")
        if (not entry["enabled"] or entry["status"] == "DISABLED") and entry["trust_level"] != "DISABLED":
            warnings.append(f"{label}: disabled state should use DISABLED trust for unambiguous routing")
        if entry["trust_level"] == "AUTHORITATIVE" and entry.get("publisher", {}).get("type") != "vendor":
            errors.append(f"{label}: AUTHORITATIVE requires a vendor publisher")
        if entry["installed"] and entry["scope"] != "external" and not Path(entry["location"]).exists():
            errors.append(f"{label}: installed registry path is unavailable: {entry['location']}")
        for dependency in entry.get("dependencies", []):
            target = by_id.get(dependency.get("id"))
            if not target and not dependency.get("optional"):
                errors.append(f"{label}: unavailable required dependency {dependency.get('id')}")
            elif target and not dependency.get("optional"):
                usable, reason = is_selectable_shallow(target)
                if not usable:
                    errors.append(f"{label}: required dependency disabled or unavailable: {dependency.get('id')} ({reason})")

        if entry["installed"] and entry["scope"] == "shared" and Path(entry["location"]).exists():
            skill_root = Path(entry["location"])
            skill_file = skill_root / "SKILL.md"
            if not skill_file.exists():
                errors.append(f"{label}: SKILL.md is missing")
                continue
            metadata, frontmatter_errors = parse_frontmatter(skill_file)
            errors.extend(frontmatter_errors)
            if metadata.get("name") != entry["id"]:
                errors.append(f"{label}: frontmatter name does not match registry id")
            if not metadata.get("description"):
                errors.append(f"{label}: frontmatter description is missing")
            text = skill_file.read_text(encoding="utf-8")
            line_count = len(text.splitlines())
            if line_count > 800:
                errors.append(f"{label}: SKILL.md exceeds 800 lines; use progressive disclosure")
            elif line_count > 400:
                warnings.append(f"{label}: SKILL.md exceeds 400 lines; review progressive disclosure")
            for link in markdown_links(text):
                if re.match(r"^[a-z]+://", link) or link.startswith("#"):
                    continue
                target = (skill_root / link).resolve()
                if not target.exists():
                    errors.append(f"{label}: broken reference link {link}")
            references = skill_root / "references"
            if references.exists():
                for reference in references.rglob("*"):
                    if reference.is_file() and reference.stat().st_size == 0:
                        errors.append(f"{label}: empty reference file {reference}")
            for script in skill_root.rglob("*.py"):
                try:
                    compile(script.read_text(encoding="utf-8"), str(script), "exec")
                except SyntaxError as exc:
                    errors.append(f"{label}: broken script {script}: {exc}")
            if run_official:
                if OFFICIAL_VALIDATOR.exists():
                    completed = subprocess.run([sys.executable, "-B", str(OFFICIAL_VALIDATOR), str(skill_root)], capture_output=True, text=True, check=False)
                    if completed.returncode != 0:
                        errors.append(f"{label}: official skill validator failed: {(completed.stdout + completed.stderr).strip()}")
                else:
                    warnings.append(f"{label}: official validator unavailable at {OFFICIAL_VALIDATOR}")

    if not DEFAULT_SCHEMA.exists() and registry_path == DEFAULT_REGISTRY:
        errors.append(f"registry schema is unavailable: {DEFAULT_SCHEMA}")
    return {"passed": not errors, "errors": errors, "warnings": warnings}


def find_entry(data: dict[str, Any], skill_id: str) -> tuple[int, dict[str, Any]]:
    for index, entry in enumerate(data.get("skills", [])):
        if entry.get("id") == skill_id:
            return index, entry
    raise ValueError(f"skill id not found: {skill_id}")


def read_entry(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if "skills" in data:
        raise ValueError("entry file must contain one skill record, not a registry")
    return data


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Personal AI OS shared-skill infrastructure")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--skip-official", action="store_true")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--capability", required=True)
    broker_parser = subparsers.add_parser("broker")
    broker_parser.add_argument("--task")
    broker_parser.add_argument("--capability", action="append", default=[])
    subparsers.add_parser("duplicates")
    for command in ("add", "update"):
        mutation = subparsers.add_parser(command)
        mutation.add_argument("--entry-file", required=True, type=Path)
    disable_parser = subparsers.add_parser("disable")
    disable_parser.add_argument("--id", required=True)
    enable_parser = subparsers.add_parser("enable")
    enable_parser.add_argument("--id", required=True)
    enable_parser.add_argument("--trust-level", choices=["AUTHORITATIVE", "VERIFIED", "COMMUNITY", "EXPERIMENTAL"], required=True)
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("--id", required=True)

    args = parser.parse_args()
    try:
        data = load_json(args.registry)
        if args.command == "list":
            print_json([{"id": entry["id"], "status": entry["status"], "trust_level": entry["trust_level"], "enabled": entry["enabled"]} for entry in data.get("skills", [])])
        elif args.command == "search":
            candidates, rejected = capability_candidates(data, args.capability)
            print_json({"capability": args.capability, "matches": [entry["id"] for entry in candidates], "rejected": rejected})
        elif args.command == "broker":
            if not args.task and not args.capability:
                raise ValueError("broker requires --task or --capability")
            print_json(broker(data, args.task, args.capability))
        elif args.command == "duplicates":
            print_json(duplicate_report(data))
        elif args.command == "validate":
            result = validate_registry(data, args.registry, run_official=not args.skip_official)
            print_json(result)
            raise SystemExit(0 if result["passed"] else 1)
        elif args.command == "add":
            entry = read_entry(args.entry_file)
            if any(existing.get("id") == entry.get("id") for existing in data.get("skills", [])):
                raise ValueError(f"skill id already exists: {entry.get('id')}")
            candidate = copy.deepcopy(data)
            candidate.setdefault("skills", []).append(entry)
            result = validate_registry(candidate, args.registry, run_official=False)
            if not result["passed"]:
                raise ValueError("new entry fails validation: " + "; ".join(result["errors"]))
            save_registry_atomic(args.registry, candidate)
            print_json({"added": entry["id"]})
        elif args.command == "update":
            entry = read_entry(args.entry_file)
            index, _ = find_entry(data, entry.get("id", ""))
            candidate = copy.deepcopy(data)
            candidate["skills"][index] = entry
            result = validate_registry(candidate, args.registry, run_official=False)
            if not result["passed"]:
                raise ValueError("updated entry fails validation: " + "; ".join(result["errors"]))
            save_registry_atomic(args.registry, candidate)
            print_json({"updated": entry["id"]})
        elif args.command == "disable":
            index, entry = find_entry(data, args.id)
            candidate = copy.deepcopy(data)
            candidate["skills"][index] = {**entry, "enabled": False, "status": "DISABLED", "trust_level": "DISABLED"}
            save_registry_atomic(args.registry, candidate)
            print_json({"disabled": args.id})
        elif args.command == "enable":
            index, entry = find_entry(data, args.id)
            candidate = copy.deepcopy(data)
            candidate["skills"][index] = {**entry, "enabled": True, "status": "AVAILABLE", "trust_level": args.trust_level}
            result = validate_registry(candidate, args.registry, run_official=False)
            if not result["passed"]:
                raise ValueError("enabled entry fails validation: " + "; ".join(result["errors"]))
            save_registry_atomic(args.registry, candidate)
            print_json({"enabled": args.id, "trust_level": args.trust_level})
        elif args.command == "remove":
            index, _ = find_entry(data, args.id)
            candidate = copy.deepcopy(data)
            candidate["skills"].pop(index)
            save_registry_atomic(args.registry, candidate)
            print_json({"removed_registry_record": args.id, "source_deleted": False})
    except ValueError as exc:
        print_json({"error": str(exc)})
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
