# How CSV jobs enter Job Searching Agent

## Recommendation

The dashboard should not use a CSV file as its permanent database. A CSV is an import and audit format. The permanent source of truth should be the Job Searching Agent database.

The safe production flow is:

`Job-search automation -> CSV or structured payload -> ingestion service -> validation and deduplication -> database -> dashboard live refresh`

## What happens after each search run

1. The job-search automation finishes its scheduled run.
2. It produces one structured record for every discovered job. This can arrive as a CSV file, a Google Sheets row, or a direct API payload.
3. An ingestion service validates required fields such as company, role, official URL, location, sponsorship evidence, DSA level, deadline, and investigation day.
4. The service creates a stable canonical job key. Official job ID or official URL is preferred. If neither exists, a normalized company, role, location, and source combination is used.
5. The service checks whether that canonical job already exists.
6. A new job is inserted once. A repeated job is updated rather than duplicated.
7. A separate observation record links the job to that search run and Day number.
8. The dashboard refreshes automatically after the database transaction completes.

## Yesterday's jobs and today's jobs

Yesterday's unfinished jobs remain in the database and in the Application Queue. They are not replaced by today's run.

Example:

- Day 31 morning: 10 shortlisted jobs are added.
- No applications are completed, so all 10 remain `Left to apply`.
- Day 31 at 18:00: 8 additional unique jobs are found.
- The database now contains 18 shortlisted jobs.
- If 3 are manually marked Applied, the Agent Dashboard shows 18 Shortlisted, 3 Applied, and 15 Left to apply.

If the 18:00 run finds one of the same morning jobs again, the job count does not increase. Its `last_seen_at` time and run history are updated.

## What is stored permanently

### Jobs

One record per unique opportunity:

- canonical job ID
- company and role
- official URL and source
- UK country, region, city, and work model
- fit result and evidence
- sponsorship state and evidence
- DSA state and evidence
- deadline
- first seen and last seen
- current queue status

### Search runs

One record per automation run:

- run ID
- Day number
- start and finish time
- companies and jobs reviewed
- completion state
- evidence gaps and agent errors
- original CSV archive location

### Job observations

One link between a job and every run in which it appeared. This preserves history without creating duplicate jobs.

### Applications

The user-controlled lifecycle:

- shortlisted
- saved
- applied
- awaiting response
- interview
- offer
- rejected
- withdrawn
- not pursuing

Each status change is appended to a timeline. Moving a job from Applied to Interview does not create another application.

## Automatic loading options

### Recommended: direct API ingestion

The search automation sends structured job records directly to a protected backend endpoint. This is the fastest and most reliable option. The CSV is still archived for audit.

### Acceptable: Google Sheets ingestion

The automation writes rows to a controlled Google Sheet. A scheduled sync or webhook imports new and changed rows into the database. The dashboard still reads from the database, not directly from the sheet.

### Fallback: CSV upload folder

The automation saves each CSV into a watched cloud-storage folder. A worker detects the new file, validates it, imports it, records the result, and archives the source file. This is useful when the automation cannot call an API.

## Why the database is necessary

- Old jobs remain available across days.
- Duplicate jobs are prevented.
- Manual application statuses are not overwritten by a later search run.
- Search history and application history remain separate.
- Counts stay accurate when jobs move between stages.
- The website can update immediately without downloading and parsing every historical CSV.
- Failed imports can be retried safely.

## Day number calculation

The Day number is calculated from the Europe/London calendar date, not from the day of the month.

- 30 Aug 2026 = Day 30
- 31 Aug 2026 = Day 31
- 1 Sep 2026 = Day 32

The counter continues across month and year boundaries.

## Production safeguard

The importer must never overwrite a manually changed application status. Search automation owns discovery evidence and latest job facts. Jyothesh Karnam owns application decisions and lifecycle status.
