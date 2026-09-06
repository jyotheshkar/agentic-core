from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPOSITORY = Path(__file__).resolve().parents[2]
HOME = Path.home()
PLUGIN_ROOT = HOME / "plugins"
AI_OS_ROOT = HOME / ".codex" / "ai-os"
SKILL_ROOT = HOME / ".codex" / "skills"
EXCLUDED_PARTS = {"__pycache__", ".cache", ".git", "node_modules"}
EXCLUDED_SUFFIXES = {".pyc", ".log", ".db", ".sqlite", ".sqlite3"}
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".yaml", ".yml", ".toml"}


def files_under(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_bytes(path: Path) -> tuple[bytes, bool]:
    raw = path.read_bytes()
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return raw, False
    text = raw.decode("utf-8")
    home_pattern = re.compile(re.escape(str(HOME)), re.IGNORECASE)
    sanitised = home_pattern.sub("<HOME>", text)
    if path.name == "aios_skills.py":
        sanitised = sanitised.replace(
            'AIOS_ROOT = Path.home() / ".codex" / "ai-os"',
            'REPOSITORY_ROOT = Path(__file__).resolve().parents[2]\nAIOS_ROOT = REPOSITORY_ROOT / "core"',
        )
    if path.name == "test_aios_skills.py":
        sanitised = sanitised.replace(
            'BIN_DIR = Path(__file__).resolve().parents[1] / "bin"',
            'BIN_DIR = Path(__file__).resolve().parents[1] / "broker"',
        )
    sanitised = sanitised.rstrip("\r\n") + "\n"
    return sanitised.encode("utf-8"), sanitised != text


def copy_tree(source: Path, destination: Path, apply: bool, manifest: list[dict[str, str]]) -> None:
    if not source.is_dir():
        raise FileNotFoundError(source)
    for source_file in files_under(source):
        relative = source_file.relative_to(source)
        destination_file = destination / relative
        output, transformed = repository_bytes(source_file)
        manifest.append(
            {
                "source": str(source_file).replace(str(HOME), "<HOME>"),
                "destination": destination_file.relative_to(REPOSITORY).as_posix(),
                "source_sha256": sha256(source_file),
                "destination_sha256": hashlib.sha256(output).hexdigest(),
                "transform": "private home path sanitised" if transformed else "none",
            }
        )
        if apply:
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            destination_file.write_bytes(output)


def sanitized_registries(apply: bool, manifest: list[dict[str, str]]) -> list[str]:
    destination = REPOSITORY / "core" / "registry"
    source = AI_OS_ROOT / "registry"
    skill_registry = json.loads((source / "skill-registry.json").read_text(encoding="utf-8"))
    agent_registry = json.loads((source / "agent-registry.json").read_text(encoding="utf-8"))

    skill_ids: list[str] = []
    for skill in skill_registry["skills"]:
        skill_id = skill["id"]
        skill_ids.append(skill_id)
        repo_location = f"core/shared-skills/{skill_id}"
        skill["location"] = repo_location
        skill.setdefault("source", {})["uri"] = repo_location
        skill["source"]["repository"] = "agentic-core"

    def redact(value):
        if isinstance(value, dict):
            return {key: redact(item) for key, item in value.items()}
        if isinstance(value, list):
            return [redact(item) for item in value]
        if isinstance(value, str) and str(HOME).lower() in value.lower():
            return "<RUNTIME_PATH_REDACTED>"
        return value

    outputs = {
        "skill-registry.json": skill_registry,
        "agent-registry.json": redact(agent_registry),
    }
    for name, payload in outputs.items():
        encoded = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        manifest.append(
            {
                "source": f"<HOME>/.codex/ai-os/registry/{name}",
                "destination": f"core/registry/{name}",
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "transform": "repository paths sanitised",
            }
        )
        if apply:
            destination.mkdir(parents=True, exist_ok=True)
            (destination / name).write_bytes(encoded)

    for name in ("skill-registry.schema.json", "agent-registry.schema.json"):
        source_file = source / name
        destination_file = destination / name
        manifest.append(
            {
                "source": str(source_file).replace(str(HOME), "<HOME>"),
                "destination": destination_file.relative_to(REPOSITORY).as_posix(),
                "sha256": sha256(source_file),
            }
        )
        if apply:
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination_file)
    return skill_ids


def main() -> int:
    parser = argparse.ArgumentParser(description="Import sanitised Agentic Core runtime sources.")
    parser.add_argument("--apply", action="store_true", help="Copy allowlisted sources into the repository.")
    args = parser.parse_args()

    for required in (PLUGIN_ROOT, AI_OS_ROOT, SKILL_ROOT):
        if not required.is_dir():
            raise FileNotFoundError(required)

    manifest: list[dict[str, str]] = []
    skill_ids = sanitized_registries(args.apply, manifest)

    for folder in ("bin", "docs", "policies", "validation"):
        destination_name = {"bin": "broker", "validation": "validation"}.get(folder, folder)
        copy_tree(AI_OS_ROOT / folder, REPOSITORY / "core" / destination_name, args.apply, manifest)

    for skill_id in skill_ids:
        copy_tree(SKILL_ROOT / skill_id, REPOSITORY / "core" / "shared-skills" / skill_id, args.apply, manifest)

    for plugin in ("minister", "scout", "forge", "moa"):
        copy_tree(PLUGIN_ROOT / plugin, REPOSITORY / "plugins" / plugin, args.apply, manifest)
    copy_tree(PLUGIN_ROOT / "devil", REPOSITORY / "plugins" / "legacy" / "devil", args.apply, manifest)

    summary = {
        "component": "agentic-core-runtime-baseline",
        "mode": "apply" if args.apply else "dry-run",
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_model": "live runtime remains authoritative",
        "file_count": len(manifest),
        "files": manifest,
        "exclusions": [
            "cache directories",
            "runtime logs",
            "database files",
            "credentials and authentication state",
            "unregistered user skills",
        ],
    }
    print(json.dumps({"mode": summary["mode"], "file_count": summary["file_count"]}, indent=2))

    if args.apply:
        record = REPOSITORY / "records" / "imports" / "agentic-core-runtime-baseline.json"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"manifest={record.relative_to(REPOSITORY).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
