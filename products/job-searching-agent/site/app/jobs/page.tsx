'use client';

import { useMemo, useState } from 'react';
import { Bookmark, ChevronRight, Filter, Search, X } from 'lucide-react';
import { AppShell } from '@/components/app-shell';
import { Deadline, DsaMeter, Flag, PageHeader, StatusBadge } from '@/components/product-ui';
import { countryLabel, enumLabel, jobs, statusLabel, type Job } from '@/lib/domain';

export default function JobsPage() {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('ALL');
  const [selected, setSelected] = useState<Job | null>(null);
  const filtered = useMemo(() => jobs.filter((job) => {
    const matchesText = `${job.company} ${job.role} ${job.city} ${job.recommendationId}`.toLowerCase().includes(query.toLowerCase());
    return matchesText && (status === 'ALL' || job.status === status);
  }), [query, status]);
  return <AppShell>
    <PageHeader title="All Jobs" description={`${jobs.length} canonical jobs · repeated sightings do not inflate totals`} />
    <div className="page-content">
      <section className="toolbar-card"><label className="search-box"><Search size={18} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search company, role, location, or ID" aria-label="Search all jobs" /></label><div className="filter-chips"><button onClick={() => setStatus('ALL')} className={status === 'ALL' ? 'active' : ''}>All {jobs.length}</button>{['SHORTLISTED','SAVED','APPLIED','INTERVIEW'].map((item) => <button key={item} onClick={() => setStatus(item)} className={status === item ? 'active' : ''}>{statusLabel(item as Job['status'])}</button>)}<button><Filter size={16} />More filters</button></div></section>
      <section className="data-card jobs-list"><header className="data-title"><div><h2>Canonical job register</h2><p>Automation evidence and your application status remain separate</p></div><span>{filtered.length} shown</span></header><div className="all-jobs-head"><span>Status</span><span>Fit</span><span>Company and role</span><span>Flag</span><span>Sponsorship</span><span>DSA</span><span>Deadline</span><span>First seen</span><span /></div>{filtered.map((job) => <button className="all-job-row" key={job.id} onClick={() => setSelected(job)}><StatusBadge value={statusLabel(job.status)} /><strong>{job.fit}</strong><span className="job-title"><strong>{job.company}</strong><span>{job.role}</span></span><Flag country={job.country} /><StatusBadge value={job.sponsorship === 'FAILED' ? 'Failed gate' : enumLabel(job.sponsorship)} /><DsaMeter level={job.dsa} /><Deadline date={job.deadline} /><span>Day {job.firstSeenDay}</span><ChevronRight size={18} /></button>)}</section>
    </div>
    {selected && <div className="drawer-backdrop"><dialog open className="job-drawer" aria-label={`${selected.role} details`}><header><div><span>{selected.recommendationId}</span><h2>{selected.role}</h2><p>{selected.company}</p></div><button aria-label="Close job details" onClick={() => setSelected(null)}><X /></button></header><div className="drawer-body"><div className="drawer-facts"><span><Flag country={selected.country} />{selected.city}, {countryLabel(selected.country)}</span><span><strong>{selected.fit}%</strong> fit</span><StatusBadge value={statusLabel(selected.status)} /></div><section><h3>Why this role fits</h3><p>{selected.rationale}</p></section><section className="warning-panel"><h3>Primary evidence gap</h3><p>{selected.gap}</p></section><section><h3>Investigation evidence</h3><dl><div><dt>Sponsorship</dt><dd>{enumLabel(selected.sponsorship)}</dd></div><div><dt>DSA</dt><dd><DsaMeter level={selected.dsa} /></dd></div><div><dt>Deadline</dt><dd><Deadline date={selected.deadline} /></dd></div><div><dt>Source</dt><dd>{selected.source}</dd></div></dl></section></div><footer><button className="button secondary"><Bookmark size={17} />Save</button><button className="button primary">Open official application</button></footer></dialog></div>}
  </AppShell>;
}
