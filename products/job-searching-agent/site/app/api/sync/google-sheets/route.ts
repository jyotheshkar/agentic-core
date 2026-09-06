import { readJobRows } from '@/lib/server/google-sheets';
import { ingestRows } from '@/lib/server/ingestion';
import { json, requireOwner } from '@/lib/server/runtime';
export async function POST(request: Request) {
  try { const actor = requireOwner(request); const rows = await readJobRows(); const result = await ingestRows(rows, 'GOOGLE_SHEETS', actor); return json(result); }
  catch (error) { if (error instanceof Response) return error; const detail = error instanceof Error ? error.message : 'Unknown error'; return json({ error: 'Google Sheets sync unavailable', detail }, { status: detail.startsWith('NEEDS REVIEW') ? 503 : 502 }); }
}
