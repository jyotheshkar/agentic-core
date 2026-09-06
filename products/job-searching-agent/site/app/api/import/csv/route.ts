import { parseCsv } from '@/lib/csv';
import { ingestRows } from '@/lib/server/ingestion';
import { json, requireOwner } from '@/lib/server/runtime';
export async function POST(request: Request) {
  try {
    const actor = requireOwner(request);
    const contentType = request.headers.get('content-type') ?? '';
    const text = contentType.includes('multipart/form-data') ? (await request.formData()).get('file') : await request.text();
    const csv = text instanceof File ? await text.text() : typeof text === 'string' ? text : '';
    if (!csv || new TextEncoder().encode(csv).byteLength > 2_000_000) return json({ error: 'CSV must be present and no larger than 2 MB' }, { status: 400 });
    const result = await ingestRows(parseCsv(csv), 'CSV', actor);
    return json(result, { status: result.batch.status === 'FAILED' ? 422 : 200 });
  } catch (error) { if (error instanceof Response) return error; return json({ error: 'CSV import failed', detail: error instanceof Error ? error.message : 'Unknown error' }, { status: 400 }); }
}
