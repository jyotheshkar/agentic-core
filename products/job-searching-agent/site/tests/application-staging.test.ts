import { describe, expect, it } from 'vitest';
import { createManualStagingPackage } from '@/lib/application-staging';

const eligibleRole = {
  jobId: 'job-verified',
  company: 'Example AI',
  role: 'Evaluation Engineer',
  officialUrl: 'https://careers.example.test/jobs/verified',
  qualification: { decision: 'APPLY' as const, applicationConfidence: 80, sponsorship: 'CONFIRMED' as const },
};

describe('manual application staging', () => {
  it('creates a review-only package for an eligible role', () => {
    expect(createManualStagingPackage(eligibleRole, { cvVersion: 'AI Evaluation V4', coverLetterDraftReady: true, applicationAnswersReviewed: true })).toMatchObject({
      state: 'READY_FOR_USER_REVIEW',
      manualOnly: true,
      package: { jobId: 'job-verified', prohibitedActions: ['NO_AUTO_SUBMISSION', 'NO_CAPTCHA_SOLVING', 'NO_EMPLOYER_CONTACT', 'NO_SPONSORSHIP_INFERENCE'] },
    });
  });

  it('makes absent user materials review tasks instead of inventing them', () => {
    const result = createManualStagingPackage(eligibleRole);
    expect(result.state).toBe('READY_FOR_USER_REVIEW');
    if (result.state === 'READY_FOR_USER_REVIEW') {
      expect(result.package.reviewTasks).toContain('Select the CV version to use.');
      expect(result.package.reviewTasks).toContain('Prepare and review a tailored cover-letter draft.');
    }
  });

  it('refuses low-confidence, unverified-sponsorship, and non-APPLY roles', () => {
    expect(createManualStagingPackage({ ...eligibleRole, qualification: { ...eligibleRole.qualification, applicationConfidence: 79 } })).toEqual({ state: 'REFUSED', reason: 'APPLICATION_CONFIDENCE_BELOW_THRESHOLD', package: null });
    expect(createManualStagingPackage({ ...eligibleRole, qualification: { ...eligibleRole.qualification, sponsorship: 'LIKELY' } })).toEqual({ state: 'REFUSED', reason: 'SPONSORSHIP_NOT_CONFIRMED', package: null });
    expect(createManualStagingPackage({ ...eligibleRole, qualification: { ...eligibleRole.qualification, decision: 'VERIFY_FIRST' } })).toEqual({ state: 'REFUSED', reason: 'DECISION_NOT_APPLY', package: null });
  });
});
