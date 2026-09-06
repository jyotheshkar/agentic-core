export const applicationStatuses = ['SHORTLISTED', 'SAVED', 'APPLIED', 'AWAITING_RESPONSE', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN', 'NOT_PURSUING'] as const;
export type ApplicationStatus = (typeof applicationStatuses)[number];
export type Country = 'ENGLAND' | 'SCOTLAND' | 'WALES' | 'NORTHERN_IRELAND';
export type DsaLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'UNKNOWN';
export type Sponsorship = 'CONFIRMED' | 'LIKELY' | 'REVIEW' | 'UNKNOWN' | 'FAILED';
export type RunStatus = 'COMPLETE' | 'PARTIAL' | 'FAILED' | 'DELAYED';
export const qualificationDecisions = ['APPLY', 'VERIFY_FIRST', 'SKIP'] as const;
export type QualificationDecision = (typeof qualificationDecisions)[number];
export const applicationConfidenceThreshold = 80;

export type PackageEligibilityReason =
  | 'ELIGIBLE_FOR_MANUAL_PREPARATION'
  | 'DECISION_NOT_APPLY'
  | 'APPLICATION_CONFIDENCE_BELOW_THRESHOLD'
  | 'SPONSORSHIP_NOT_CONFIRMED';

export interface RoleQualification {
  decision: QualificationDecision;
  applicationConfidence: number;
  sponsorship: Sponsorship;
}

export interface PackageEligibility {
  eligible: boolean;
  reason: PackageEligibilityReason;
}

/**
 * This is intentionally a local preparation gate. It does not submit an
 * application, contact anyone, or infer sponsorship evidence.
 */
export function evaluateManualPackageEligibility(qualification: RoleQualification): PackageEligibility {
  if (qualification.decision !== 'APPLY') return { eligible: false, reason: 'DECISION_NOT_APPLY' };
  if (qualification.applicationConfidence < applicationConfidenceThreshold) return { eligible: false, reason: 'APPLICATION_CONFIDENCE_BELOW_THRESHOLD' };
  if (qualification.sponsorship !== 'CONFIRMED') return { eligible: false, reason: 'SPONSORSHIP_NOT_CONFIRMED' };
  return { eligible: true, reason: 'ELIGIBLE_FOR_MANUAL_PREPARATION' };
}

export interface Job {
  id: string;
  source: string;
  sourceJobId: string;
  company: string;
  role: string;
  city: string;
  country: Country;
  workModel: 'On-site' | 'Hybrid' | 'Remote';
  fit: number;
  sponsorship: Sponsorship;
  dsa: DsaLevel;
  deadline: string | null;
  firstSeenDay: number;
  recommendationId: string;
  status: ApplicationStatus;
  rationale: string;
  gap: string;
}

export const jobs: Job[] = [
  { id: 'job-001', source: 'Official careers', sourceJobId: 'NS-2408', company: 'Northstar AI Lab', role: 'Senior AI Evaluation Engineer', city: 'London', country: 'ENGLAND', workModel: 'Hybrid', fit: 92, sponsorship: 'CONFIRMED', dsa: 'MEDIUM', deadline: '2026-09-08', firstSeenDay: 35, recommendationId: 'JSA-0037-001', status: 'SHORTLISTED', rationale: 'Direct match for LLM evaluation, adversarial testing, Python, and model-quality operations.', gap: 'Evidence of leading a formal assurance programme is limited.' },
  { id: 'job-002', source: 'Official careers', sourceJobId: 'CRI-911', company: 'Caledonia Research Institute', role: 'Research Data Scientist', city: 'Edinburgh', country: 'SCOTLAND', workModel: 'Hybrid', fit: 89, sponsorship: 'LIKELY', dsa: 'LOW', deadline: '2026-09-11', firstSeenDay: 36, recommendationId: 'JSA-0037-002', status: 'SAVED', rationale: 'Strong research-methodology, statistical evaluation, and Python alignment.', gap: 'Published research is desirable and needs positioning.' },
  { id: 'job-003', source: 'Civil Service Jobs', sourceJobId: 'CPS-881', company: 'Cymru Public Sector AI', role: 'AI Assurance Analyst', city: 'Cardiff', country: 'WALES', workModel: 'Hybrid', fit: 86, sponsorship: 'REVIEW', dsa: 'LOW', deadline: '2026-09-15', firstSeenDay: 37, recommendationId: 'JSA-0037-003', status: 'SHORTLISTED', rationale: 'Good fit for safety evaluation, evidence review, and red-team workflows.', gap: 'Sponsorship wording is not explicit.' },
  { id: 'job-004', source: 'Official careers', sourceJobId: 'UDS-771', company: 'Ulster Digital Systems', role: 'LLM Quality Engineer', city: 'Belfast', country: 'NORTHERN_IRELAND', workModel: 'Remote', fit: 84, sponsorship: 'UNKNOWN', dsa: 'MEDIUM', deadline: '2026-09-18', firstSeenDay: 37, recommendationId: 'JSA-0037-004', status: 'SHORTLISTED', rationale: 'Strong match for evaluation design and multi-modal quality assessment.', gap: 'Algorithm interview depth is not published.' },
  { id: 'job-005', source: 'Official careers', sourceJobId: 'VER-502', company: 'Verity Systems', role: 'Responsible AI Consultant', city: 'Manchester', country: 'ENGLAND', workModel: 'Hybrid', fit: 82, sponsorship: 'LIKELY', dsa: 'LOW', deadline: '2026-09-21', firstSeenDay: 34, recommendationId: 'JSA-0034-005', status: 'APPLIED', rationale: 'Relevant responsible AI, evaluation, and stakeholder communication work.', gap: 'Consulting delivery examples need to be explicit.' },
  { id: 'job-006', source: 'Official careers', sourceJobId: 'HZN-144', company: 'Horizon Compute', role: 'Machine Learning Evaluator', city: 'Cambridge', country: 'ENGLAND', workModel: 'On-site', fit: 80, sponsorship: 'CONFIRMED', dsa: 'HIGH', deadline: '2026-09-24', firstSeenDay: 33, recommendationId: 'JSA-0033-006', status: 'AWAITING_RESPONSE', rationale: 'Foundation-model evaluation experience is directly relevant.', gap: 'High DSA preparation requirement.' },
  { id: 'job-007', source: 'Official careers', sourceJobId: 'SFT-908', company: 'SafeTech Analytics', role: 'AI Red Team Specialist', city: 'Bristol', country: 'ENGLAND', workModel: 'Remote', fit: 90, sponsorship: 'CONFIRMED', dsa: 'MEDIUM', deadline: '2026-09-26', firstSeenDay: 31, recommendationId: 'JSA-0031-007', status: 'INTERVIEW', rationale: 'Excellent match for adversarial testing and red-team experience.', gap: 'Security framework examples should be prepared.' },
  { id: 'job-008', source: 'Official careers', sourceJobId: 'NOVA-208', company: 'Nova Insight Group', role: 'AI Governance Associate', city: 'Leeds', country: 'ENGLAND', workModel: 'Hybrid', fit: 77, sponsorship: 'FAILED', dsa: 'UNKNOWN', deadline: null, firstSeenDay: 30, recommendationId: 'JSA-0030-008', status: 'NOT_PURSUING', rationale: 'Some policy and evaluation alignment.', gap: 'Employer does not provide sponsorship for this vacancy.' },
];

export const investigations = [
  { day: 37, date: '6 Sep 2026', status: 'COMPLETE' as RunStatus, companies: 16, reviewed: 20, actionable: 4, scotland: 1, applied: 0, excluded: 16, gaps: 2, errors: 0, score: 94 },
  { day: 36, date: '5 Sep 2026', status: 'PARTIAL' as RunStatus, companies: 13, reviewed: 18, actionable: 3, scotland: 1, applied: 1, excluded: 15, gaps: 4, errors: 1, score: 86 },
  { day: 35, date: '4 Sep 2026', status: 'COMPLETE' as RunStatus, companies: 18, reviewed: 24, actionable: 5, scotland: 2, applied: 1, excluded: 19, gaps: 1, errors: 0, score: 96 },
  { day: 34, date: '3 Sep 2026', status: 'DELAYED' as RunStatus, companies: 10, reviewed: 12, actionable: 2, scotland: 0, applied: 0, excluded: 10, gaps: 3, errors: 0, score: 81 },
];

export const statusLabel = (status: ApplicationStatus) => status.toLowerCase().split('_').map((part) => part[0].toUpperCase() + part.slice(1)).join(' ');
export const countrySlug = (country: Country) => country.toLowerCase().replaceAll('_', '-');
export const countryLabel = (country: Country) => ({ ENGLAND: 'England', SCOTLAND: 'Scotland', WALES: 'Wales', NORTHERN_IRELAND: 'Northern Ireland' })[country];
export const enumLabel = (value: string) => value.toLowerCase().split('_').map((part) => part[0].toUpperCase() + part.slice(1)).join(' ');
