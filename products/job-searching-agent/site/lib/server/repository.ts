import { countryLabel, jobs as fixtures, investigations, type Job } from '@/lib/domain';
import { descriptiveOutcomeAnalytics, type OutcomeObservation } from '@/lib/analytics';
import { orderedTimeline, scheduledManualFollowUps, type ApplicationTimelineEvent, type FollowUpRecord } from '@/lib/follow-up';
import { dashboardMetrics } from '@/lib/metrics';
import { runtimeEnv } from './runtime';

type DbJobRow = {
  id: string; source: string; source_job_id: string; company: string; role: string; city: string; country: Job['country']; work_model: Job['workModel']; first_seen_day: number;
  fit_score: number; sponsorship: Job['sponsorship']; dsa: Job['dsa']; deadline: string | null; rationale: string; gap: string; status: Job['status'];
};

export async function listJobs(): Promise<{ records: Job[]; source: 'D1' | 'SYNTHETIC' }> {
  try {
    const result = await runtimeEnv().DB.prepare(`
      SELECT j.id, j.source, COALESCE(j.source_job_id, '') source_job_id, j.company, j.role, j.city, j.country, j.work_model, j.first_seen_day,
             e.fit_score, e.sponsorship, e.dsa, e.deadline, e.rationale, e.gap,
             COALESCE(a.status, 'SHORTLISTED') status
      FROM jobs j
      JOIN job_evidence e ON e.id = (SELECT e2.id FROM job_evidence e2 WHERE e2.job_id = j.id ORDER BY e2.created_at DESC LIMIT 1)
      LEFT JOIN applications a ON a.job_id = j.id
      WHERE j.closed_at IS NULL
      ORDER BY e.fit_score DESC, e.deadline ASC
    `).all<DbJobRow>();
    if (!result.results?.length) return { records: fixtures, source: 'SYNTHETIC' };
    return { source: 'D1', records: result.results.map((row) => ({ id: row.id, source: row.source, sourceJobId: row.source_job_id, company: row.company, role: row.role, city: row.city, country: row.country, workModel: row.work_model, fit: row.fit_score, sponsorship: row.sponsorship, dsa: row.dsa, deadline: row.deadline, firstSeenDay: row.first_seen_day, recommendationId: row.id, status: row.status, rationale: row.rationale, gap: row.gap })) };
  } catch {
    return { records: fixtures, source: 'SYNTHETIC' };
  }
}

export async function findJob(jobId: string) {
  const { records, source } = await listJobs();
  return { record: records.find((job) => job.id === jobId) ?? null, source };
}

export async function dashboardData() {
  const { records, source } = await listJobs();
  return { source, generatedAt: new Date().toISOString(), metrics: dashboardMetrics(records), priorityJobs: records.filter((job) => ['SHORTLISTED','SAVED'].includes(job.status)).slice(0,4), countries: records.map((job) => countryLabel(job.country)) };
}

export async function investigationData() {
  try {
    const result = await runtimeEnv().DB.prepare(`SELECT day_number day, substr(started_at, 1, 10) date, status, companies_investigated companies, jobs_reviewed reviewed, actionable_jobs actionable, error_count errors FROM search_runs ORDER BY day_number DESC LIMIT 60`).all();
    if (result.results?.length) return { source: 'D1', records: result.results };
  } catch {}
  return { source: 'SYNTHETIC', records: investigations };
}

export async function applicationTimeline(jobId: string) {
  try {
    const result = await runtimeEnv().DB.prepare(`
      SELECT e.id, e.from_status fromStatus, e.to_status toStatus, e.note, e.occurred_at occurredAt
      FROM application_events e
      JOIN applications a ON a.id = e.application_id
      WHERE a.job_id = ?
      ORDER BY e.occurred_at DESC
      LIMIT 100
    `).bind(jobId).all<ApplicationTimelineEvent>();
    return { source: 'D1' as const, records: orderedTimeline(result.results ?? []) };
  } catch {
    return { source: 'SYNTHETIC' as const, records: [] };
  }
}

export async function manualFollowUps(now = new Date()) {
  try {
    const result = await runtimeEnv().DB.prepare(`
      SELECT a.id applicationId, a.job_id jobId, j.company, j.role, a.status, a.follow_up_at followUpAt
      FROM applications a
      JOIN jobs j ON j.id = a.job_id
      WHERE a.follow_up_at IS NOT NULL
      ORDER BY a.follow_up_at ASC
      LIMIT 100
    `).all<FollowUpRecord>();
    return { source: 'D1' as const, records: scheduledManualFollowUps(result.results ?? [], now) };
  } catch {
    return { source: 'SYNTHETIC' as const, records: [] };
  }
}

export async function outcomeAnalytics() {
  try {
    const result = await runtimeEnv().DB.prepare(`
      SELECT j.role_type roleType, j.city, j.country, e.fit_score fitScore, a.status
      FROM applications a
      JOIN jobs j ON j.id = a.job_id
      JOIN job_evidence e ON e.id = (SELECT e2.id FROM job_evidence e2 WHERE e2.job_id = j.id ORDER BY e2.created_at DESC LIMIT 1)
      ORDER BY a.updated_at DESC
      LIMIT 5000
    `).all<OutcomeObservation>();
    return { source: 'D1' as const, ...descriptiveOutcomeAnalytics(result.results ?? []) };
  } catch {
    return { source: 'SYNTHETIC' as const, ...descriptiveOutcomeAnalytics([]) };
  }
}
