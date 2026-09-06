import { evaluateManualPackageEligibility, type RoleQualification } from './domain';

export interface StagingRole {
  jobId: string;
  company: string;
  role: string;
  officialUrl: string;
  qualification: RoleQualification;
}

export interface UserMaterialsState {
  cvVersion?: string;
  coverLetterDraftReady?: boolean;
  applicationAnswersReviewed?: boolean;
}

export type ManualStagingPackage =
  | { state: 'REFUSED'; reason: string; package: null }
  | {
      state: 'READY_FOR_USER_REVIEW';
      manualOnly: true;
      package: {
        jobId: string;
        company: string;
        role: string;
        officialUrl: string;
        reviewTasks: string[];
        prohibitedActions: readonly ['NO_AUTO_SUBMISSION', 'NO_CAPTCHA_SOLVING', 'NO_EMPLOYER_CONTACT', 'NO_SPONSORSHIP_INFERENCE'];
      };
    };

/**
 * Produces local review metadata only. It does not write a file, use a browser,
 * submit an application, contact an employer, or infer immigration eligibility.
 */
export function createManualStagingPackage(role: StagingRole, materials: UserMaterialsState = {}): ManualStagingPackage {
  const eligibility = evaluateManualPackageEligibility(role.qualification);
  if (!eligibility.eligible) return { state: 'REFUSED', reason: eligibility.reason, package: null };

  const reviewTasks = [
    'Re-open the official vacancy and confirm it remains live.',
    'Confirm every mandatory eligibility requirement using user-provided evidence.',
    'Review sponsorship evidence manually before relying on it.',
  ];
  if (!materials.cvVersion) reviewTasks.push('Select the CV version to use.');
  if (!materials.coverLetterDraftReady) reviewTasks.push('Prepare and review a tailored cover-letter draft.');
  if (!materials.applicationAnswersReviewed) reviewTasks.push('Review every application answer before any manual submission.');

  return {
    state: 'READY_FOR_USER_REVIEW',
    manualOnly: true,
    package: {
      jobId: role.jobId,
      company: role.company,
      role: role.role,
      officialUrl: role.officialUrl,
      reviewTasks,
      prohibitedActions: ['NO_AUTO_SUBMISSION', 'NO_CAPTCHA_SOLVING', 'NO_EMPLOYER_CONTACT', 'NO_SPONSORSHIP_INFERENCE'],
    },
  };
}
