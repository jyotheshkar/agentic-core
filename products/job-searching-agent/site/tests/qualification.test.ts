import { describe, expect, it } from 'vitest';
import { applicationConfidenceThreshold, countryLabel, evaluateManualPackageEligibility } from '@/lib/domain';

describe('manual package qualification', () => {
  it('allows only the explicit APPLY, confirmed-sponsorship, 80-or-higher boundary', () => {
    expect(evaluateManualPackageEligibility({ decision: 'APPLY', applicationConfidence: applicationConfidenceThreshold, sponsorship: 'CONFIRMED' })).toEqual({ eligible: true, reason: 'ELIGIBLE_FOR_MANUAL_PREPARATION' });
  });

  it('fails closed below the application-confidence boundary', () => {
    expect(evaluateManualPackageEligibility({ decision: 'APPLY', applicationConfidence: applicationConfidenceThreshold - 1, sponsorship: 'CONFIRMED' })).toEqual({ eligible: false, reason: 'APPLICATION_CONFIDENCE_BELOW_THRESHOLD' });
  });

  it('does not treat non-APPLY decisions as preparation authority', () => {
    expect(evaluateManualPackageEligibility({ decision: 'VERIFY_FIRST', applicationConfidence: 100, sponsorship: 'CONFIRMED' })).toEqual({ eligible: false, reason: 'DECISION_NOT_APPLY' });
    expect(evaluateManualPackageEligibility({ decision: 'SKIP', applicationConfidence: 100, sponsorship: 'CONFIRMED' })).toEqual({ eligible: false, reason: 'DECISION_NOT_APPLY' });
  });

  it('does not infer sponsorship evidence from likely, review, unknown, or failed states', () => {
    for (const sponsorship of ['LIKELY', 'REVIEW', 'UNKNOWN', 'FAILED'] as const) {
      expect(evaluateManualPackageEligibility({ decision: 'APPLY', applicationConfidence: 100, sponsorship })).toEqual({ eligible: false, reason: 'SPONSORSHIP_NOT_CONFIRMED' });
    }
  });

  it('preserves the four UK country labels used by qualification and reporting', () => {
    expect([countryLabel('ENGLAND'), countryLabel('SCOTLAND'), countryLabel('WALES'), countryLabel('NORTHERN_IRELAND')]).toEqual(['England', 'Scotland', 'Wales', 'Northern Ireland']);
  });
});
