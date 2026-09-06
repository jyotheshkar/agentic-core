# Agent Registry Contract

The shared Agent Registry is separate from the Skill Registry. It records installed and legacy agent plugins without fabricating future agents.

Selectable records must be enabled, AVAILABLE, installed, dependency-satisfied, and trusted for the requested action. Disabled, NOT_INSTALLED, BLOCKED, or planned records are excluded. Public capability plugins can be discovered natively but are not treated as autonomous agents without supporting metadata.

Core records are Minister, Scout, Forge, MOA, and Devil in its actual legacy not-installed state. New agents become routable by adding one validated record. Duplicate IDs, false paths, false installed states, and unavailable dependencies fail health validation.
