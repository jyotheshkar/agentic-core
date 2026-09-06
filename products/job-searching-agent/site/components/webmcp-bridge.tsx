'use client';
import { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { applicationStatuses, statusLabel, type ApplicationStatus } from '@/lib/domain';

declare global {
  interface Document {
    modelContext?: { registerTool(tool: { name: string; title?: string; description: string; inputSchema: object; annotations?: { readOnlyHint?: boolean; untrustedContentHint?: boolean }; execute(input: unknown): unknown }, options?: { signal?: AbortSignal }): unknown };
  }
}

type StagedChange = { jobId: string; status: ApplicationStatus };

export function WebMcpBridge() {
  const [staged, setStaged] = useState<StagedChange | null>(null);
  const [result, setResult] = useState('');
  useEffect(() => {
    const context = document.modelContext;
    if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    const register = (tool: Parameters<typeof context.registerTool>[0]) => { try { void Promise.resolve(context.registerTool(tool, { signal: lifecycle.signal })); } catch {} };
    register({ name: 'get_priority_jobs', title: 'Get priority jobs', description: 'Read the current highest-priority jobs visible in Job Searching Agent.', inputSchema: { type: 'object', properties: {}, additionalProperties: false }, annotations: { readOnlyHint: true, untrustedContentHint: true }, async execute() { const response = await fetch('/api/jobs?status=SHORTLISTED'); const data = await response.json() as { source?: string; records?: { id: string; company: string; role: string; fit: number }[] }; return { source: data.source, jobs: data.records?.slice(0,5).map((job) => ({ id: job.id, company: job.company, role: job.role, fit: job.fit })) ?? [] }; } });
    register({ name: 'refresh_job_data', title: 'Refresh job data', description: 'Run the same Google Sheets refresh shown by the visible Refresh control.', inputSchema: { type: 'object', properties: {}, additionalProperties: false }, annotations: { readOnlyHint: false, untrustedContentHint: true }, async execute() { const response = await fetch('/api/sync/google-sheets', { method: 'POST' }); return { status: response.ok ? 'refreshed' : 'needs_review', detail: await response.json() }; } });
    register({ name: 'stage_application_status_change', title: 'Stage application status', description: 'Open a visible confirmation for an application status change. This never commits before Jyothesh Karnam confirms it.', inputSchema: { type: 'object', properties: { jobId: { type: 'string' }, status: { type: 'string', enum: [...applicationStatuses] } }, required: ['jobId','status'], additionalProperties: false }, annotations: { readOnlyHint: false, untrustedContentHint: false }, execute(input) { const value = input as Partial<StagedChange>; if (!value.jobId || !value.status || !applicationStatuses.includes(value.status)) throw new Error('Invalid job or status'); setStaged({ jobId: value.jobId, status: value.status }); return { status: 'awaiting_user_confirmation', jobId: value.jobId, proposedStatus: value.status }; } });
    return () => lifecycle.abort();
  }, []);
  const confirm = async () => { if (!staged) return; const response = await fetch(`/api/jobs/${encodeURIComponent(staged.jobId)}/application`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ status: staged.status }) }); setResult(response.ok ? `Status changed to ${statusLabel(staged.status)}.` : 'The change could not be saved.'); setStaged(null); };
  if (!staged && !result) return null;
  return <>{staged && <div className="confirmation-backdrop"><section className="confirmation-card" role="alertdialog" aria-modal="true" aria-labelledby="status-confirm-title"><header><h2 id="status-confirm-title">Confirm status change</h2><button aria-label="Cancel status change" onClick={() => setStaged(null)}><X /></button></header><p>Change job <strong>{staged.jobId}</strong> to <strong>{statusLabel(staged.status)}</strong>?</p><small>This action records a permanent application event. It does not submit a job application or contact anyone.</small><footer><button className="button secondary" onClick={() => setStaged(null)}>Cancel</button><button className="button primary" onClick={confirm}>Confirm change</button></footer></section></div>}{result && <button className="undo-toast" onClick={() => setResult('')}>{result}<span>Dismiss</span></button>}</>;
}
