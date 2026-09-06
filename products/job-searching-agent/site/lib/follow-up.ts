import type { ApplicationStatus } from './domain';

export interface ApplicationTimelineEvent {
  id: string;
  fromStatus: ApplicationStatus | null;
  toStatus: ApplicationStatus;
  note: string | null;
  occurredAt: string;
}

export interface FollowUpRecord {
  applicationId: string;
  jobId: string;
  company: string;
  role: string;
  status: ApplicationStatus;
  followUpAt: string | null;
}

export interface ManualFollowUp extends FollowUpRecord {
  due: boolean;
}

const closedStatuses = new Set<ApplicationStatus>(['REJECTED', 'WITHDRAWN', 'NOT_PURSUING']);

export function orderedTimeline(events: ApplicationTimelineEvent[]) {
  return [...events].sort((left, right) => right.occurredAt.localeCompare(left.occurredAt));
}

/** Returns manual work only. It does not send a reminder or contact anyone. */
export function scheduledManualFollowUps(records: FollowUpRecord[], now = new Date()) {
  const nowIso = now.toISOString();
  return records
    .filter((record) => record.followUpAt !== null && !closedStatuses.has(record.status))
    .map((record) => ({ ...record, due: record.followUpAt! <= nowIso }))
    .sort((left, right) => left.followUpAt!.localeCompare(right.followUpAt!));
}
