import { describe, expect, it } from 'vitest';
import { jobs } from '@/lib/domain';
import { dashboardMetrics } from '@/lib/metrics';

describe('cumulative dashboard metrics', () => {
  it('keeps interview applications inside the Applied total', () => {
    const metrics = dashboardMetrics(jobs);
    expect(metrics.applied).toBe(3);
    expect(metrics.byCountry.ENGLAND).toBe(3);
  });
  it('never reports daily application counters', () => {
    const metrics = dashboardMetrics(jobs) as Record<string, unknown>;
    expect(metrics.appliedToday).toBeUndefined();
    expect(metrics.appliedYesterday).toBeUndefined();
  });
});
