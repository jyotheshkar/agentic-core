import type { Job } from './domain';

const appliedStates = new Set(['APPLIED', 'AWAITING_RESPONSE', 'INTERVIEW', 'OFFER', 'REJECTED', 'WITHDRAWN']);

export function dashboardMetrics(records: Job[], overallScans = 112) {
  const shortlist = records.filter((job) => !['NOT_PURSUING'].includes(job.status));
  const applied = records.filter((job) => appliedStates.has(job.status));
  return {
    shortlisted: shortlist.length,
    applied: applied.length,
    leftToApply: shortlist.filter((job) => !appliedStates.has(job.status)).length,
    overallScans,
    byCountry: {
      ENGLAND: applied.filter((job) => job.country === 'ENGLAND').length,
      SCOTLAND: applied.filter((job) => job.country === 'SCOTLAND').length,
      WALES: applied.filter((job) => job.country === 'WALES').length,
      NORTHERN_IRELAND: applied.filter((job) => job.country === 'NORTHERN_IRELAND').length,
    },
  };
}
