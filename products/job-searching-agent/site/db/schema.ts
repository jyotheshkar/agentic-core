import { sql } from 'drizzle-orm';
import { index, integer, primaryKey, sqliteTable, text, uniqueIndex } from 'drizzle-orm/sqlite-core';

const timestamps = {
  createdAt: text('created_at').notNull().default(sql`(CURRENT_TIMESTAMP)`),
  updatedAt: text('updated_at').notNull().default(sql`(CURRENT_TIMESTAMP)`),
};

export const jobs = sqliteTable('jobs', {
  id: text('id').primaryKey(),
  source: text('source').notNull(),
  sourceJobId: text('source_job_id'),
  officialUrl: text('official_url'),
  company: text('company').notNull(),
  role: text('role').notNull(),
  roleType: text('role_type', { enum: ['AI_ML','DATA','RESEARCH','GOVERNANCE','OTHER'] }).notNull(),
  city: text('city').notNull(),
  country: text('country', { enum: ['ENGLAND','SCOTLAND','WALES','NORTHERN_IRELAND'] }).notNull(),
  workModel: text('work_model', { enum: ['On-site','Hybrid','Remote'] }).notNull(),
  firstSeenDay: integer('first_seen_day').notNull(),
  closedAt: text('closed_at'),
  ...timestamps,
}, (table) => [
  uniqueIndex('jobs_source_job_id_uq').on(table.source, table.sourceJobId),
  uniqueIndex('jobs_official_url_uq').on(table.officialUrl),
  index('jobs_country_idx').on(table.country),
  index('jobs_day_idx').on(table.firstSeenDay),
]);

export const searchRuns = sqliteTable('search_runs', {
  id: text('id').primaryKey(),
  dayNumber: integer('day_number').notNull(),
  startedAt: text('started_at').notNull(),
  completedAt: text('completed_at'),
  status: text('status', { enum: ['COMPLETE','PARTIAL','FAILED','DELAYED'] }).notNull(),
  companiesInvestigated: integer('companies_investigated').notNull().default(0),
  jobsReviewed: integer('jobs_reviewed').notNull().default(0),
  actionableJobs: integer('actionable_jobs').notNull().default(0),
  errorCount: integer('error_count').notNull().default(0),
  ...timestamps,
}, (table) => [uniqueIndex('search_runs_day_uq').on(table.dayNumber), index('search_runs_status_idx').on(table.status)]);

export const jobObservations = sqliteTable('job_observations', {
  id: text('id').primaryKey(),
  jobId: text('job_id').notNull().references(() => jobs.id, { onDelete: 'cascade' }),
  runId: text('run_id').notNull().references(() => searchRuns.id, { onDelete: 'cascade' }),
  observedAt: text('observed_at').notNull(),
  sourceRowKey: text('source_row_key').notNull(),
  sourceChecksum: text('source_checksum').notNull(),
  ...timestamps,
}, (table) => [uniqueIndex('observations_run_row_uq').on(table.runId, table.sourceRowKey), index('observations_job_idx').on(table.jobId)]);

export const jobEvidence = sqliteTable('job_evidence', {
  id: text('id').primaryKey(),
  jobId: text('job_id').notNull().references(() => jobs.id, { onDelete: 'cascade' }),
  fitScore: integer('fit_score').notNull(),
  applicationConfidence: integer('application_confidence').notNull(),
  decision: text('decision', { enum: ['APPLY','VERIFY_FIRST','SKIP'] }).notNull(),
  sponsorship: text('sponsorship', { enum: ['CONFIRMED','LIKELY','REVIEW','UNKNOWN','FAILED'] }).notNull(),
  dsa: text('dsa', { enum: ['LOW','MEDIUM','HIGH','UNKNOWN'] }).notNull(),
  salary: text('salary'),
  deadline: text('deadline'),
  rationale: text('rationale').notNull(),
  gap: text('gap').notNull(),
  verifiedAt: text('verified_at'),
  ...timestamps,
}, (table) => [index('evidence_job_idx').on(table.jobId), index('evidence_fit_idx').on(table.fitScore), index('evidence_sponsorship_idx').on(table.sponsorship)]);

export const applications = sqliteTable('applications', {
  id: text('id').primaryKey(),
  jobId: text('job_id').notNull().references(() => jobs.id, { onDelete: 'restrict' }),
  status: text('status', { enum: ['SHORTLISTED','SAVED','APPLIED','AWAITING_RESPONSE','INTERVIEW','OFFER','REJECTED','WITHDRAWN','NOT_PURSUING'] }).notNull(),
  appliedAt: text('applied_at'),
  cvVersion: text('cv_version'),
  coverLetterState: text('cover_letter_state'),
  followUpAt: text('follow_up_at'),
  recruiterContact: text('recruiter_contact'),
  notes: text('notes'),
  outcome: text('outcome'),
  ...timestamps,
}, (table) => [uniqueIndex('applications_job_uq').on(table.jobId), index('applications_status_idx').on(table.status)]);

export const applicationEvents = sqliteTable('application_events', {
  id: text('id').primaryKey(),
  applicationId: text('application_id').notNull().references(() => applications.id, { onDelete: 'cascade' }),
  fromStatus: text('from_status'),
  toStatus: text('to_status').notNull(),
  changedBy: text('changed_by').notNull(),
  note: text('note'),
  occurredAt: text('occurred_at').notNull(),
}, (table) => [index('application_events_app_idx').on(table.applicationId, table.occurredAt)]);

export const ingestionBatches = sqliteTable('ingestion_batches', {
  id: text('id').primaryKey(),
  source: text('source', { enum: ['GOOGLE_SHEETS','CSV'] }).notNull(),
  checksum: text('checksum').notNull(),
  rowsReceived: integer('rows_received').notNull(),
  rowsAccepted: integer('rows_accepted').notNull().default(0),
  rowsQuarantined: integer('rows_quarantined').notNull().default(0),
  status: text('status', { enum: ['VALIDATING','IMPORTED','PARTIAL','FAILED'] }).notNull(),
  errorSummary: text('error_summary'),
  importedAt: text('imported_at'),
  ...timestamps,
}, (table) => [uniqueIndex('ingestion_checksum_uq').on(table.source, table.checksum)]);

export const supervisorReviews = sqliteTable('supervisor_reviews', {
  id: text('id').primaryKey(),
  runId: text('run_id').notNull().references(() => searchRuns.id, { onDelete: 'cascade' }),
  score: integer('score').notNull(),
  findings: text('findings').notNull(),
  errorCount: integer('error_count').notNull().default(0),
  evidenceGapCount: integer('evidence_gap_count').notNull().default(0),
  reviewedAt: text('reviewed_at').notNull(),
}, (table) => [uniqueIndex('supervisor_reviews_run_uq').on(table.runId)]);

export const agentVersions = sqliteTable('agent_versions', {
  id: text('id').primaryKey(),
  version: text('version').notNull(),
  state: text('state', { enum: ['PRODUCTION','CANDIDATE','PROMOTED','REJECTED'] }).notNull(),
  evidence: text('evidence'),
  decidedAt: text('decided_at'),
  ...timestamps,
}, (table) => [uniqueIndex('agent_versions_version_uq').on(table.version)]);

export const dailyDigests = sqliteTable('daily_digests', {
  id: text('id').primaryKey(),
  dayNumber: integer('day_number').notNull(),
  subject: text('subject').notNull(),
  summary: text('summary').notNull(),
  deliveryState: text('delivery_state', { enum: ['PREPARED','SENT','FAILED','NOT_REQUESTED'] }).notNull(),
  connectorReceiptId: text('connector_receipt_id'),
  deliveredAt: text('delivered_at'),
  ...timestamps,
}, (table) => [uniqueIndex('daily_digests_day_uq').on(table.dayNumber)]);

export const settings = sqliteTable('settings', {
  key: text('key').primaryKey(),
  value: text('value').notNull(),
  ownerId: text('owner_id').notNull(),
  updatedAt: text('updated_at').notNull().default(sql`(CURRENT_TIMESTAMP)`),
});

export const auditEvents = sqliteTable('audit_events', {
  id: text('id').primaryKey(),
  actorId: text('actor_id').notNull(),
  action: text('action').notNull(),
  entityType: text('entity_type').notNull(),
  entityId: text('entity_id').notNull(),
  payload: text('payload').notNull(),
  occurredAt: text('occurred_at').notNull(),
}, (table) => [index('audit_entity_idx').on(table.entityType, table.entityId), index('audit_time_idx').on(table.occurredAt)]);

export const quarantinedRows = sqliteTable('quarantined_rows', {
  batchId: text('batch_id').notNull().references(() => ingestionBatches.id, { onDelete: 'cascade' }),
  rowNumber: integer('row_number').notNull(),
  reason: text('reason').notNull(),
  safePreview: text('safe_preview').notNull(),
}, (table) => [primaryKey({ columns: [table.batchId, table.rowNumber] })]);
