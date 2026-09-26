# Agentic Core Runtime Excerpt

This is a sanitized excerpt of the actual newer MVP, preserving five core modules and two original synthetic test modules. It is an engineering demonstration, not a complete native plugin installation.

Use Python 3.11 or later, then install requirements.txt into a local virtual environment and run:

```powershell
python -B -m unittest discover -s tests -p "test_core*.py" -v
```

Fresh exported-source result:35 tests PASS. Tests construct synthetic cases inline and use temporary SQLite state. No model call, mailbox action or business send is executed.

Read core/contracts.py for typed packages and lifecycle; core/algorithms.py for bounded routing/evidence/risk/utility calculations; core/safety.py for dispatch and path/redaction checks; core/engine.py for SQLite execution, receipts, retries and checkpoints. The host remains responsible for reasoning. Locally attested receipts are not provider signatures. No distributed exactly-once behavior is established.

Full native release evidence is separate:60 tests,100 source-derived skill packages,11 role plugins and small native synthetic demonstrations. Those omitted components cannot be inferred as available from this excerpt. See Source Manifest.json and Attribution.md.
