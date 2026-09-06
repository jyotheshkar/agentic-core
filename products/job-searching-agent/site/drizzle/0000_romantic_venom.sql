CREATE TABLE `agent_versions` (
	`id` text PRIMARY KEY NOT NULL,
	`version` text NOT NULL,
	`state` text NOT NULL,
	`evidence` text,
	`decided_at` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `agent_versions_version_uq` ON `agent_versions` (`version`);--> statement-breakpoint
CREATE TABLE `application_events` (
	`id` text PRIMARY KEY NOT NULL,
	`application_id` text NOT NULL,
	`from_status` text,
	`to_status` text NOT NULL,
	`changed_by` text NOT NULL,
	`note` text,
	`occurred_at` text NOT NULL,
	FOREIGN KEY (`application_id`) REFERENCES `applications`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE INDEX `application_events_app_idx` ON `application_events` (`application_id`,`occurred_at`);--> statement-breakpoint
CREATE TABLE `applications` (
	`id` text PRIMARY KEY NOT NULL,
	`job_id` text NOT NULL,
	`status` text NOT NULL,
	`applied_at` text,
	`cv_version` text,
	`cover_letter_state` text,
	`follow_up_at` text,
	`recruiter_contact` text,
	`notes` text,
	`outcome` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	FOREIGN KEY (`job_id`) REFERENCES `jobs`(`id`) ON UPDATE no action ON DELETE restrict
);
--> statement-breakpoint
CREATE UNIQUE INDEX `applications_job_uq` ON `applications` (`job_id`);--> statement-breakpoint
CREATE INDEX `applications_status_idx` ON `applications` (`status`);--> statement-breakpoint
CREATE TABLE `audit_events` (
	`id` text PRIMARY KEY NOT NULL,
	`actor_id` text NOT NULL,
	`action` text NOT NULL,
	`entity_type` text NOT NULL,
	`entity_id` text NOT NULL,
	`payload` text NOT NULL,
	`occurred_at` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `audit_entity_idx` ON `audit_events` (`entity_type`,`entity_id`);--> statement-breakpoint
CREATE INDEX `audit_time_idx` ON `audit_events` (`occurred_at`);--> statement-breakpoint
CREATE TABLE `daily_digests` (
	`id` text PRIMARY KEY NOT NULL,
	`day_number` integer NOT NULL,
	`subject` text NOT NULL,
	`summary` text NOT NULL,
	`delivery_state` text NOT NULL,
	`connector_receipt_id` text,
	`delivered_at` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `daily_digests_day_uq` ON `daily_digests` (`day_number`);--> statement-breakpoint
CREATE TABLE `ingestion_batches` (
	`id` text PRIMARY KEY NOT NULL,
	`source` text NOT NULL,
	`checksum` text NOT NULL,
	`rows_received` integer NOT NULL,
	`rows_accepted` integer DEFAULT 0 NOT NULL,
	`rows_quarantined` integer DEFAULT 0 NOT NULL,
	`status` text NOT NULL,
	`error_summary` text,
	`imported_at` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `ingestion_checksum_uq` ON `ingestion_batches` (`source`,`checksum`);--> statement-breakpoint
CREATE TABLE `job_evidence` (
	`id` text PRIMARY KEY NOT NULL,
	`job_id` text NOT NULL,
	`fit_score` integer NOT NULL,
	`decision` text NOT NULL,
	`sponsorship` text NOT NULL,
	`dsa` text NOT NULL,
	`salary` text,
	`deadline` text,
	`rationale` text NOT NULL,
	`gap` text NOT NULL,
	`verified_at` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	FOREIGN KEY (`job_id`) REFERENCES `jobs`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE INDEX `evidence_job_idx` ON `job_evidence` (`job_id`);--> statement-breakpoint
CREATE INDEX `evidence_fit_idx` ON `job_evidence` (`fit_score`);--> statement-breakpoint
CREATE INDEX `evidence_sponsorship_idx` ON `job_evidence` (`sponsorship`);--> statement-breakpoint
CREATE TABLE `job_observations` (
	`id` text PRIMARY KEY NOT NULL,
	`job_id` text NOT NULL,
	`run_id` text NOT NULL,
	`observed_at` text NOT NULL,
	`source_row_key` text NOT NULL,
	`source_checksum` text NOT NULL,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	FOREIGN KEY (`job_id`) REFERENCES `jobs`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`run_id`) REFERENCES `search_runs`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `observations_run_row_uq` ON `job_observations` (`run_id`,`source_row_key`);--> statement-breakpoint
CREATE INDEX `observations_job_idx` ON `job_observations` (`job_id`);--> statement-breakpoint
CREATE TABLE `jobs` (
	`id` text PRIMARY KEY NOT NULL,
	`source` text NOT NULL,
	`source_job_id` text,
	`official_url` text,
	`company` text NOT NULL,
	`role` text NOT NULL,
	`city` text NOT NULL,
	`country` text NOT NULL,
	`work_model` text NOT NULL,
	`first_seen_day` integer NOT NULL,
	`closed_at` text,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `jobs_source_job_id_uq` ON `jobs` (`source`,`source_job_id`);--> statement-breakpoint
CREATE UNIQUE INDEX `jobs_official_url_uq` ON `jobs` (`official_url`);--> statement-breakpoint
CREATE INDEX `jobs_country_idx` ON `jobs` (`country`);--> statement-breakpoint
CREATE INDEX `jobs_day_idx` ON `jobs` (`first_seen_day`);--> statement-breakpoint
CREATE TABLE `quarantined_rows` (
	`batch_id` text NOT NULL,
	`row_number` integer NOT NULL,
	`reason` text NOT NULL,
	`safe_preview` text NOT NULL,
	PRIMARY KEY(`batch_id`, `row_number`),
	FOREIGN KEY (`batch_id`) REFERENCES `ingestion_batches`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `search_runs` (
	`id` text PRIMARY KEY NOT NULL,
	`day_number` integer NOT NULL,
	`started_at` text NOT NULL,
	`completed_at` text,
	`status` text NOT NULL,
	`companies_investigated` integer DEFAULT 0 NOT NULL,
	`jobs_reviewed` integer DEFAULT 0 NOT NULL,
	`actionable_jobs` integer DEFAULT 0 NOT NULL,
	`error_count` integer DEFAULT 0 NOT NULL,
	`created_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `search_runs_day_uq` ON `search_runs` (`day_number`);--> statement-breakpoint
CREATE INDEX `search_runs_status_idx` ON `search_runs` (`status`);--> statement-breakpoint
CREATE TABLE `settings` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL,
	`owner_id` text NOT NULL,
	`updated_at` text DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
--> statement-breakpoint
CREATE TABLE `supervisor_reviews` (
	`id` text PRIMARY KEY NOT NULL,
	`run_id` text NOT NULL,
	`score` integer NOT NULL,
	`findings` text NOT NULL,
	`error_count` integer DEFAULT 0 NOT NULL,
	`evidence_gap_count` integer DEFAULT 0 NOT NULL,
	`reviewed_at` text NOT NULL,
	FOREIGN KEY (`run_id`) REFERENCES `search_runs`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `supervisor_reviews_run_uq` ON `supervisor_reviews` (`run_id`);