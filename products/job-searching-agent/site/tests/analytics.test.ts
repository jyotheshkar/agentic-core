import { describe, expect, it } from 'vitest';
import { descriptiveOutcomeAnalytics, fitScoreBand } from '@/lib/analytics';

describe('descriptive outcome analytics', () => {
  it('keeps sparse groups explicitly insufficient and leaves policy unchanged', () => {
    const result = descriptiveOutcomeAnalytics([
      { roleType: 'AI_ML', city: 'London', country: 'ENGLAND', fitScore: 92, status: 'INTERVIEW' },
      { roleType: 'AI_ML', city: 'London', country: 'ENGLAND', fitScore: 88, status: 'REJECTED' },
    ]);
    expect(result.policyChange).toBe('NO_POLICY_CHANGE');
    expect(result.recommendedAction).toBe('COLLECT_MORE_EXPLICIT_OUTCOMES');
    expect(result.roleType[0]).toMatchObject({ key: 'AI_ML', applications: 2, observedResponses: 2, responseRate: null, evidenceStatus: 'INSUFFICIENT_EVIDENCE' });
  });

  it('reports response rates only after enough explicit application outcomes', () => {
    const result = descriptiveOutcomeAnalytics([
      { roleType: 'DATA', city: 'Edinburgh', country: 'SCOTLAND', fitScore: 81, status: 'INTERVIEW' },
      { roleType: 'DATA', city: 'Edinburgh', country: 'SCOTLAND', fitScore: 83, status: 'REJECTED' },
      { roleType: 'DATA', city: 'Edinburgh', country: 'SCOTLAND', fitScore: 85, status: 'AWAITING_RESPONSE' },
      { roleType: 'DATA', city: 'Edinburgh', country: 'SCOTLAND', fitScore: 86, status: 'APPLIED' },
      { roleType: 'DATA', city: 'Edinburgh', country: 'SCOTLAND', fitScore: 89, status: 'OFFER' },
    ]);
    expect(result.roleType[0]).toMatchObject({ key: 'DATA', applications: 5, observedResponses: 3, interviews: 1, offers: 1, rejections: 1, responseRate: 0.6, evidenceStatus: 'SUFFICIENT_FOR_DESCRIPTION' });
    expect(result.location[0].key).toBe('Edinburgh, SCOTLAND');
  });

  it('uses deterministic score bands without changing any qualification threshold', () => {
    expect([fitScoreBand(100), fitScoreBand(90), fitScoreBand(80), fitScoreBand(70), fitScoreBand(0)]).toEqual(['90-100', '90-100', '80-89', '70-79', '0-69']);
  });
});
