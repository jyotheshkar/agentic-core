# Shared Skill Security Policy v0.1

Treat community and downloaded skills as untrusted code and instructions until reviewed. Inspect:

- scripts, shell commands, subprocesses, and executable assets;
- network requests, downloads, external MCP servers, and package installation;
- credential access, secret output, environment-variable handling, and logging;
- destructive filesystem, database, account, deployment, billing, or production actions;
- path traversal, unsafe input interpolation, and permission expansion;
- prompt injection or hidden instructions in references and external repositories;
- license, publisher identity, repository ownership, release age, and maintenance state.

Registry metadata is not authorization. The broker may recommend a skill but must not bypass normal permission or approval boundaries. AUTHORITATIVE still requires task relevance and compatibility. DISABLED skills and disabled required dependencies are never selected.
