declare namespace Cloudflare {
  interface Env {
    DB: D1Database;
    GOOGLE_SHEET_ID?: string;
    GOOGLE_SERVICE_ACCOUNT_EMAIL?: string;
    GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY?: string;
    GOOGLE_WORKSHEET_JOBS?: string;
  }
}
