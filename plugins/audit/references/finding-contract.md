# Audit Finding Contract

Every finding contains: stable identifier, title, severity (`INFO`, `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`), inspectable evidence identifier or link, confidence from 0 to 1, limitations, recommendation, and escalation conditions.

Use `APPROVE`, `APPROVE WITH CONDITIONS`, `REWORK`, `DEFER`, or `BLOCKED`. Evidence gaps that could reverse an assurance conclusion require `DEFER`; unresolved high or critical findings require `REWORK`.
