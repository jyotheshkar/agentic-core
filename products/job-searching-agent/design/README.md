# Job Searching Agent, Frontend UI and UX Design

This folder is the complete design review package for Job Searching Agent V 3.0.

Open **UI Design Gallery.html** first. It displays every page in desktop and mobile format in the intended navigation order.

## Screen inventory

1. Agent Dashboard
2. All Jobs
3. Application Queue
4. Applications
5. Daily Investigations
6. Agent Performance
7. Settings

Each numbered folder contains:

- `Desktop.png`, the 1440 x 1024 desktop direction.
- `Mobile.png`, the 390 x 844 responsive direction.

## Important design decisions

- The visible product wordmark is **Job Searching Agent**.
- The application version remains **V 3.0** in the desktop sidebar and mobile More menu.
- The main Overview page is titled **Agent Dashboard**.
- The filled Agent Dashboard uses clearly labelled sample data. It is not live campaign evidence.
- Compact locations use flags. England, Scotland, Wales, and Northern Ireland are counted separately.
- The Union Flag represents Northern Ireland and will receive an accessible Northern Ireland label and tooltip in production.
- DSA uses exactly five segments: one green for low, three orange for medium, five red for high, and five gray outlines for unknown.
- Deadlines use a clock icon and visible text.
- Green means confirmed or successful. Orange means review or caution. Red means urgent, failed, closed, or rejected. Gray means unknown or inactive.
- Colour is never the only signal. Every state also includes an icon and label.

## Day number rule

The Day number is a continuous campaign counter in the Europe/London timezone. It does not restart when a new month begins.

- 30 Aug 2026 = Day 30
- 31 Aug 2026 = Day 31
- 1 Sep 2026 = Day 32
- 2 Sep 2026 = Day 33

The production calculation is:

`Day N = 30 + number of Europe/London calendar days since 30 Aug 2026`

## Data note

The current files are UI designs only. They do not connect to Google Sheets, CSV files, a database, email, or automations. The intended production data flow is documented in `08 - Data Flow/How CSV Jobs Enter the Dashboard.md`.
