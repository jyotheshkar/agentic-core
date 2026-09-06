import { describe, expect, it } from 'vitest';
import { orderedTimeline, scheduledManualFollowUps } from '@/lib/follow-up';

describe('manual follow-up and status projections', () => {
  it('orders append-only timeline events newest first without mutating the input', () => {
    const events = [
      { id: 'older', fromStatus: 'APPLIED' as const, toStatus: 'AWAITING_RESPONSE' as const, note: null, occurredAt: '2026-09-01T09:00:00.000Z' },
      { id: 'newer', fromStatus: 'AWAITING_RESPONSE' as const, toStatus: 'INTERVIEW' as const, note: 'User supplied', occurredAt: '2026-09-02T09:00:00.000Z' },
    ];
    expect(orderedTimeline(events).map((event) => event.id)).toEqual(['newer', 'older']);
    expect(events.map((event) => event.id)).toEqual(['older', 'newer']);
  });

  it('surfaces due and scheduled manual work, but excludes terminal statuses and missing dates', () => {
    const records = [
      { applicationId: 'due', jobId: 'job-1', company: 'Northstar', role: 'Evaluator', status: 'AWAITING_RESPONSE' as const, followUpAt: '2026-09-06T08:00:00.000Z' },
      { applicationId: 'scheduled', jobId: 'job-2', company: 'SafeTech', role: 'Red Team Specialist', status: 'INTERVIEW' as const, followUpAt: '2026-09-07T08:00:00.000Z' },
      { applicationId: 'rejected', jobId: 'job-3', company: 'Closed', role: 'Analyst', status: 'REJECTED' as const, followUpAt: '2026-09-05T08:00:00.000Z' },
      { applicationId: 'none', jobId: 'job-4', company: 'No Date', role: 'Engineer', status: 'APPLIED' as const, followUpAt: null },
    ];
    expect(scheduledManualFollowUps(records, new Date('2026-09-06T12:00:00.000Z'))).toEqual([
      { ...records[0], due: true },
      { ...records[1], due: false },
    ]);
  });
});
