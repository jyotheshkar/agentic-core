# Job Search Agent

Test-mode investigation and application preparation with a cumulative queue.

Read OPERATING_CONTRACT.md for the two tasks' complete operating rules.

The local queue is working infrastructure, not a claim that any employer form is ready. Scheduled agents supply verified research, document generation and browser actions using their connected tools. agent_queue.py deliberately cannot submit applications or send email itself.

Run `python agent_queue.py init` to initialize/export. Run `python agent_queue.py list` to read records. Records enter through `ingest --file FILE`. Pack/form evidence enters through `prepare --id ID --file FILE`. Run `stage`, `outbox`, `claim`, `sent` and `unknown` for the email transaction protocol. Read OPERATING_CONTRACT.md before recording statuses.

Job Applications/applications.csv is cumulative. Job Applications/ready_to_submit.csv contains only the current ready subset. Source CVs and old Google histories remain untouched. Data Science and consultancy are in scope when actual requirements fit.

Test mode emails after five new qualified roles and individually for a verified completed draft. Production-time switching requires Jyo's explicit instruction. Automatic final submission is never enabled.
