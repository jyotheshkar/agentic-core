import Link from 'next/link';
import { Bookmark, CalendarDays, CircleOff, Clock3, Search, Send } from 'lucide-react';
import { AppShell } from '@/components/app-shell';
import { Deadline, DemoPill, DsaMeter, Flag, PageHeader } from '@/components/product-ui';
import { jobs } from '@/lib/domain';
import { investigationDay } from '@/lib/day';
import { dashboardMetrics } from '@/lib/metrics';
import { SyncControl } from '@/components/sync-control';

export default function DashboardPage() {
  const priorityJobs = jobs.filter((job) => ['SHORTLISTED', 'SAVED'].includes(job.status)).sort((a,b) => b.fit - a.fit).slice(0,4);
  const metrics = dashboardMetrics(jobs);
  const day = investigationDay();
  return <AppShell>
    <PageHeader title="Agent Dashboard" description="Automatic source check every 60 seconds while open" showDay><SyncControl automatic /><DemoPill /></PageHeader>
    <div className="content">
      <section className="top-grid">
        <div className="metrics-card">{[[metrics.shortlisted,'Shortlisted'],[metrics.applied,'Applied'],[metrics.leftToApply,'Left to apply'],[metrics.overallScans,'Overall job scans']].map(([value,label]) => <div className="metric" key={label}><strong>{value}</strong><span>{label}</span></div>)}</div>
        <div className="country-card"><h2>Applied by UK country</h2><div className="country-grid">{(['ENGLAND','SCOTLAND','WALES','NORTHERN_IRELAND'] as const).map((country) => <div className="country-count" key={country}><Flag country={country} /><strong>{metrics.byCountry[country]}</strong><span>{country === 'NORTHERN_IRELAND' ? 'Northern Ireland' : country[0]+country.slice(1).toLowerCase()}</span></div>)}</div></div>
      </section>
      <section className="attention" aria-label="Deadline warning"><span className="attention-icon"><Clock3 size={23} /></span><div><strong>3 deadlines need attention</strong><span>Review the priority queue before 8 Sep</span></div><Link href="/queue" className="button secondary">Review urgent jobs</Link></section>
      <section className="priority-card"><div className="section-heading"><div><h2>Priority applications</h2><p>Highest-value shortlisted jobs, ranked for manual application</p></div><Link href="/queue" className="button primary">Apply next</Link></div><div className="job-table" aria-label="Priority applications"><div className="job-head"><span>Fit</span><span>Company and role</span><span>Flag</span><span>Sponsorship</span><span>DSA</span><span>Deadline</span><span>Action</span></div>{priorityJobs.map((job,index) => <article className="job-row" key={job.id}><strong className="fit">{job.fit}</strong><div className="job-title"><strong>{job.company}</strong><span>{job.role}</span></div><Flag country={job.country} /><span className={`tone-${job.sponsorship === 'CONFIRMED' || job.sponsorship === 'LIKELY' ? 'success' : job.sponsorship === 'REVIEW' ? 'warning' : 'neutral'}`}>{job.sponsorship[0]+job.sponsorship.slice(1).toLowerCase()}</span><DsaMeter level={job.dsa} /><Deadline date={job.deadline} /><div className="job-actions"><Link href={`/jobs/${job.id}`} className={index === 0 ? 'small-apply primary' : 'small-apply'}>Apply</Link><button aria-label={`Save ${job.role}`}><Bookmark size={19} /></button><button aria-label={`Do not pursue ${job.role}`}><CircleOff size={19} /></button></div></article>)}</div></section>
      <section className="day-summary"><span><CalendarDays />Day {day}</span><span><Search />20 new jobs added</span><span><Bookmark />{metrics.shortlisted} shortlisted</span><span><Send />{metrics.applied} applied</span><small>SYNTHETIC DATA · PERMANENT HISTORY</small></section>
    </div>
  </AppShell>;
}
