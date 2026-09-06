import { z } from 'zod';
import { applicationStatuses } from '@/lib/domain';
import { id, runtimeEnv } from './runtime';

export const applicationUpdateSchema = z.object({
  status: z.enum(applicationStatuses),
  cvVersion: z.string().trim().max(120).nullable().optional(),
  coverLetterState: z.string().trim().max(120).nullable().optional(),
  followUpAt: z.iso.datetime().nullable().optional(),
  recruiterContact: z.string().trim().max(240).nullable().optional(),
  notes: z.string().trim().max(4000).nullable().optional(),
  outcome: z.string().trim().max(2000).nullable().optional(),
});

export async function updateApplication(jobId: string, actor: string, input: z.infer<typeof applicationUpdateSchema>) {
  const db = runtimeEnv().DB;
  const now = new Date().toISOString();
  const existing = await db.prepare('SELECT id, status FROM applications WHERE job_id = ?').bind(jobId).first<{ id: string; status: string }>();
  const applicationId = existing?.id ?? id('app');
  const appliedAt = ['APPLIED','AWAITING_RESPONSE','INTERVIEW','OFFER','REJECTED','WITHDRAWN'].includes(input.status) ? now : null;
  const statements = [
    db.prepare(`INSERT INTO applications (id, job_id, status, applied_at, cv_version, cover_letter_state, follow_up_at, recruiter_contact, notes, outcome, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(job_id) DO UPDATE SET status=excluded.status, cv_version=COALESCE(excluded.cv_version, applications.cv_version), cover_letter_state=COALESCE(excluded.cover_letter_state, applications.cover_letter_state), follow_up_at=excluded.follow_up_at, recruiter_contact=COALESCE(excluded.recruiter_contact, applications.recruiter_contact), notes=COALESCE(excluded.notes, applications.notes), outcome=COALESCE(excluded.outcome, applications.outcome), applied_at=COALESCE(applications.applied_at, excluded.applied_at), updated_at=excluded.updated_at`)
      .bind(applicationId, jobId, input.status, appliedAt, input.cvVersion ?? null, input.coverLetterState ?? null, input.followUpAt ?? null, input.recruiterContact ?? null, input.notes ?? null, input.outcome ?? null, now, now),
    db.prepare('INSERT INTO application_events (id, application_id, from_status, to_status, changed_by, note, occurred_at) VALUES (?, ?, ?, ?, ?, ?, ?)').bind(id('evt'), applicationId, existing?.status ?? null, input.status, actor, input.notes ?? null, now),
    db.prepare('INSERT INTO audit_events (id, actor_id, action, entity_type, entity_id, payload, occurred_at) VALUES (?, ?, ?, ?, ?, ?, ?)').bind(id('audit'), actor, 'APPLICATION_STATUS_CHANGED', 'job', jobId, JSON.stringify({ from: existing?.status ?? null, to: input.status }), now),
  ];
  await db.batch(statements);
  return { applicationId, previousStatus: existing?.status ?? null, status: input.status, changedAt: now };
}
