import type { ApplicationStatus, Country } from './domain';

export const roleTypes = ['AI_ML', 'DATA', 'RESEARCH', 'GOVERNANCE', 'OTHER'] as const;
export type RoleType = (typeof roleTypes)[number];

export interface OutcomeObservation {
  roleType: RoleType;
  city: string;
  country: Country;
  fitScore: number;
  status: ApplicationStatus;
}

type Dimension = 'ROLE_TYPE' | 'LOCATION' | 'FIT_SCORE_BAND';
export interface OutcomeSummary {
  dimension: Dimension;
  key: string;
  applications: number;
  observedResponses: number;
  interviews: number;
  offers: number;
  rejections: number;
  responseRate: number | null;
  evidenceStatus: 'SUFFICIENT_FOR_DESCRIPTION' | 'INSUFFICIENT_EVIDENCE';
}

const appliedStatuses = new Set<ApplicationStatus>(['APPLIED', 'AWAITING_RESPONSE', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN']);
const responseStatuses = new Set<ApplicationStatus>(['INTERVIEW', 'OFFER', 'REJECTED']);
const minimumDescriptiveSample = 5;

export function fitScoreBand(score: number) {
  if (score >= 90) return '90-100';
  if (score >= 80) return '80-89';
  if (score >= 70) return '70-79';
  return '0-69';
}

function summarize(dimension: Dimension, keyOf: (record: OutcomeObservation) => string, observations: OutcomeObservation[]): OutcomeSummary[] {
  const groups = new Map<string, OutcomeObservation[]>();
  for (const observation of observations.filter((item) => appliedStatuses.has(item.status))) {
    const key = keyOf(observation);
    groups.set(key, [...(groups.get(key) ?? []), observation]);
  }
  return [...groups.entries()].sort(([left], [right]) => left.localeCompare(right)).map(([key, records]) => {
    const observedResponses = records.filter((record) => responseStatuses.has(record.status)).length;
    const interviews = records.filter((record) => record.status === 'INTERVIEW').length;
    const offers = records.filter((record) => record.status === 'OFFER').length;
    const rejections = records.filter((record) => record.status === 'REJECTED').length;
    const evidenceStatus = records.length >= minimumDescriptiveSample ? 'SUFFICIENT_FOR_DESCRIPTION' : 'INSUFFICIENT_EVIDENCE';
    return {
      dimension,
      key,
      applications: records.length,
      observedResponses,
      interviews,
      offers,
      rejections,
      responseRate: evidenceStatus === 'SUFFICIENT_FOR_DESCRIPTION' ? observedResponses / records.length : null,
      evidenceStatus,
    };
  });
}

/** Descriptive only. This function cannot change a policy, threshold, or ranking. */
export function descriptiveOutcomeAnalytics(observations: OutcomeObservation[]) {
  return {
    policyChange: 'NO_POLICY_CHANGE' as const,
    recommendedAction: 'COLLECT_MORE_EXPLICIT_OUTCOMES' as const,
    roleType: summarize('ROLE_TYPE', (record) => record.roleType, observations),
    location: summarize('LOCATION', (record) => `${record.city}, ${record.country}`, observations),
    fitScoreBand: summarize('FIT_SCORE_BAND', (record) => fitScoreBand(record.fitScore), observations),
  };
}
