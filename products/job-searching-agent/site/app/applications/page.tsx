'use client';

import { useMemo, useState } from 'react';
import { CalendarClock, ChevronRight, FileCheck2, MessageSquareText } from 'lucide-react';
import { AppShell } from '@/components/app-shell';
import { Flag, PageHeader, StatusBadge } from '@/components/product-ui';
import { jobs, statusLabel, type ApplicationStatus } from '@/lib/domain';

const stages: { label: string; values: ApplicationStatus[] }[] = [
  { label: 'Applied', values: ['APPLIED'] },
  { label: 'Awaiting response', values: ['AWAITING_RESPONSE'] },
  { label: 'Interview', values: ['INTERVIEW'] },
  { label: 'Offer', values: ['OFFER'] },
  { label: 'Rejected', values: ['REJECTED'] },
  { label: 'Withdrawn', values: ['WITHDRAWN'] },
];

export default function ApplicationsPage() {
  const [stage, setStage] = useState('All active');
  const applications = jobs.filter((job) => ['APPLIED','AWAITING_RESPONSE','INTERVIEW','OFFER','REJECTED','WITHDRAWN'].includes(job.status));
  const shown = useMemo(() => stage === 'All active' ? applications : applications.filter((job) => stages.find((item) => item.label === stage)?.values.includes(job.status)), [stage, applications]);
  return <AppShell><PageHeader title="Applications" description={`${applications.length} cumulative applications · status changes preserve the original application count`} /><div className="page-content"><section className="stage-grid"><button className={stage === 'All active' ? 'active' : ''} onClick={() => setStage('All active')}><strong>{applications.length}</strong><span>All active</span></button>{stages.map((item) => { const count = applications.filter((job) => item.values.includes(job.status)).length; return <button key={item.label} className={stage === item.label ? 'active' : ''} onClick={() => setStage(item.label)}><strong>{count}</strong><span>{item.label}</span></button>; })}</section><section className="data-card application-list"><header className="data-title"><div><h2>Application progress</h2><p>Your manually managed application lifecycle</p></div><span>{shown.length} shown</span></header>{shown.map((job,index) => <article className="application-row" key={job.id}><div className="application-company"><Flag country={job.country} /><span><strong>{job.role}</strong><small>{job.company} · {job.city}</small></span></div><StatusBadge value={statusLabel(job.status)} /><div><small>Applied</small><strong>{index === 0 ? '3 Sep 2026' : '31 Aug 2026'}</strong></div><div><small>CV version</small><strong>{index === 0 ? 'AI Evaluation V4' : 'Technical V3'}</strong></div><div><small>Follow-up</small><strong className={index === 0 ? 'tone-warning' : ''}>{index === 0 ? '9 Sep' : 'Not scheduled'}</strong></div><button aria-label={`Open ${job.role} application`}><ChevronRight /></button></article>)}</section><section className="applications-bottom"><article className="data-card next-actions"><h2>Next actions</h2><div><CalendarClock /><span><strong>Follow up with Verity Systems</strong><small>Due in 3 days</small></span><button>Review</button></div><div><MessageSquareText /><span><strong>Prepare SafeTech interview</strong><small>Technical interview · 10 Sep</small></span><button>Prepare</button></div></article><article className="data-card record-policy"><FileCheck2 /><h2>Stable application history</h2><p>When an application advances to interview or offer, it remains part of the cumulative Applied count. Every change is written to the timeline.</p></article></section></div></AppShell>;
}
