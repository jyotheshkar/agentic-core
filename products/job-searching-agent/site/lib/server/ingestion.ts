import { z } from 'zod';
import type { ImportRow } from '@/lib/csv';
import { id, runtimeEnv } from './runtime';

const rowSchema = z.object({
  source: z.string().trim().min(1).max(160),
  source_job_id: z.string().trim().max(240).optional().default(''),
  official_url: z.url().optional().or(z.literal('')).default(''),
  company: z.string().trim().min(1).max(240),
  role: z.string().trim().min(1).max(240),
  role_type: z.enum(['AI_ML','DATA','RESEARCH','GOVERNANCE','OTHER']),
  city: z.string().trim().min(1).max(160),
  country: z.enum(['ENGLAND','SCOTLAND','WALES','NORTHERN_IRELAND']),
  work_model: z.enum(['On-site','Hybrid','Remote']),
  fit_score: z.coerce.number().int().min(0).max(100),
  application_confidence: z.coerce.number().int().min(0).max(100),
  decision: z.enum(['APPLY','VERIFY_FIRST','SKIP']),
  sponsorship: z.enum(['CONFIRMED','LIKELY','REVIEW','UNKNOWN','FAILED']),
  dsa: z.enum(['LOW','MEDIUM','HIGH','UNKNOWN']),
  deadline: z.iso.date().optional().or(z.literal('')).default(''),
  rationale: z.string().trim().min(1).max(4000),
  gap: z.string().trim().min(1).max(2000),
  day_number: z.coerce.number().int().min(1).max(100000),
});

function normalize(value: string) { return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim(); }
async function sha256(value: string) { const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value)); return [...new Uint8Array(bytes)].map((byte) => byte.toString(16).padStart(2,'0')).join(''); }

export async function ingestRows(rawRows: ImportRow[], source: 'CSV' | 'GOOGLE_SHEETS', actor: string) {
  const db = runtimeEnv().DB;
  const batchChecksum = await sha256(JSON.stringify(rawRows));
  const previous = await db.prepare('SELECT id, status, rows_accepted accepted, rows_quarantined quarantined FROM ingestion_batches WHERE source = ? AND checksum = ?').bind(source, batchChecksum).first();
  if (previous) return { idempotent: true, batch: previous };
  const batchId = id('batch');
  const now = new Date().toISOString();
  await db.prepare('INSERT INTO ingestion_batches (id, source, checksum, rows_received, rows_accepted, rows_quarantined, status, created_at, updated_at) VALUES (?, ?, ?, ?, 0, 0, ?, ?, ?)').bind(batchId, source, batchChecksum, rawRows.length, 'VALIDATING', now, now).run();
  let accepted = 0, quarantined = 0;
  const errors: { row: number; reason: string }[] = [];
  for (let index = 0; index < rawRows.length; index++) {
    const parsed = rowSchema.safeParse(rawRows[index]);
    if (!parsed.success) {
      quarantined++; const reason = parsed.error.issues.map((issue) => `${issue.path.join('.')}: ${issue.message}`).join('; ').slice(0,1000); errors.push({ row: index + 2, reason });
      await db.prepare('INSERT INTO quarantined_rows (batch_id, row_number, reason, safe_preview) VALUES (?, ?, ?, ?)').bind(batchId, index + 2, reason, JSON.stringify({ company: rawRows[index].company ?? '', role: rawRows[index].role ?? '' })).run();
      continue;
    }
    const row = parsed.data;
    const identity = row.source_job_id ? `${normalize(row.source)}|id|${normalize(row.source_job_id)}` : row.official_url ? `url|${normalize(row.official_url)}` : `${normalize(row.source)}|${normalize(row.company)}|${normalize(row.role)}|${normalize(row.city)}`;
    const jobId = `job_${(await sha256(identity)).slice(0,24)}`;
    const runId = `run_day_${row.day_number}`;
    const evidenceId = id('evidence');
    const observationId = id('observation');
    const rowChecksum = await sha256(JSON.stringify(row));
    await db.batch([
      db.prepare(`INSERT INTO search_runs (id, day_number, started_at, completed_at, status, created_at, updated_at) VALUES (?, ?, ?, ?, 'PARTIAL', ?, ?) ON CONFLICT(day_number) DO NOTHING`).bind(runId, row.day_number, now, now, now, now),
      db.prepare(`INSERT INTO jobs (id, source, source_job_id, official_url, company, role, role_type, city, country, work_model, first_seen_day, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET company=excluded.company, role=excluded.role, role_type=excluded.role_type, city=excluded.city, country=excluded.country, work_model=excluded.work_model, official_url=COALESCE(excluded.official_url, jobs.official_url), updated_at=excluded.updated_at`).bind(jobId, row.source, row.source_job_id || null, row.official_url || null, row.company, row.role, row.role_type, row.city, row.country, row.work_model, row.day_number, now, now),
      db.prepare(`INSERT INTO job_evidence (id, job_id, fit_score, application_confidence, decision, sponsorship, dsa, deadline, rationale, gap, verified_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).bind(evidenceId, jobId, row.fit_score, row.application_confidence, row.decision, row.sponsorship, row.dsa, row.deadline || null, row.rationale, row.gap, now, now, now),
      db.prepare(`INSERT INTO job_observations (id, job_id, run_id, observed_at, source_row_key, source_checksum, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(run_id, source_row_key) DO NOTHING`).bind(observationId, jobId, runId, now, `${source}:${index + 2}:${jobId}`, rowChecksum, now, now),
      db.prepare(`INSERT INTO applications (id, job_id, status, created_at, updated_at) VALUES (?, ?, 'SHORTLISTED', ?, ?) ON CONFLICT(job_id) DO NOTHING`).bind(id('app'), jobId, now, now),
    ]);
    accepted++;
  }
  const status = quarantined === 0 ? 'IMPORTED' : accepted === 0 ? 'FAILED' : 'PARTIAL';
  await db.batch([
    db.prepare('UPDATE ingestion_batches SET rows_accepted=?, rows_quarantined=?, status=?, error_summary=?, imported_at=?, updated_at=? WHERE id=?').bind(accepted, quarantined, status, errors.length ? JSON.stringify(errors.slice(0,20)) : null, now, now, batchId),
    db.prepare('INSERT INTO audit_events (id, actor_id, action, entity_type, entity_id, payload, occurred_at) VALUES (?, ?, ?, ?, ?, ?, ?)').bind(id('audit'), actor, 'INGESTION_COMPLETED', 'ingestion_batch', batchId, JSON.stringify({ source, accepted, quarantined }), now),
  ]);
  return { idempotent: false, batch: { id: batchId, status, received: rawRows.length, accepted, quarantined }, errors };
}
