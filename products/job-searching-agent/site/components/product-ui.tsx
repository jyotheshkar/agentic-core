import Link from 'next/link';
import Image from 'next/image';
import { Check, Clock3, RefreshCw } from 'lucide-react';
import { countryLabel, countrySlug, type Country, type DsaLevel } from '@/lib/domain';
import { investigationDay, londonDateLabel } from '@/lib/day';

export function DemoPill() { return <span className="demo-label">SYNTHETIC DEMO · NOT LIVE</span>; }

export function DayCard() {
  const now = new Date();
  const day = investigationDay(now);
  return <section className="day-card" aria-label={`Today is Day ${day}`}><strong>DAY {day}</strong><span>{londonDateLabel(now)}</span><small>LIVE · EUROPE/LONDON</small></section>;
}

export function PageHeader({ title, description, children, showDay = false }: { title: string; description: string; children?: React.ReactNode; showDay?: boolean }) {
  return <header className={showDay ? 'dashboard-header' : 'page-header'}>{showDay && <DayCard />}<section className="heading-block"><p className="eyebrow">JOB SEARCHING AGENT</p><h1>{title}</h1><div className="sync-line"><span className="status-check"><Check size={20} strokeWidth={3} /></span><div><strong>Data ready</strong><span>{description}</span></div></div></section><div className="header-actions">{children ?? <><button className="button secondary"><RefreshCw size={17} />Refresh</button><DemoPill /></>}</div></header>;
}

export function Flag({ country }: { country: Country }) {
  const label = countryLabel(country);
  return <span className="flag-wrap" title={label}><Image src={`/flags/${countrySlug(country)}.svg`} alt={`${label} flag`} width={58} height={36} /></span>;
}

const dsaLevel = { LOW: 1, MEDIUM: 3, HIGH: 5, UNKNOWN: 0 } satisfies Record<DsaLevel, number>;
export function DsaMeter({ level }: { level: DsaLevel }) {
  const value = dsaLevel[level];
  const tone = level === 'HIGH' ? 'danger' : level === 'MEDIUM' ? 'warning' : level === 'LOW' ? 'success' : 'neutral';
  return <fieldset className={`dsa-meter ${tone}`} title={`${level} DSA`}><legend className="sr-only">{level === 'UNKNOWN' ? 'Unknown' : level.toLowerCase()} DSA</legend>{[1,2,3,4,5].map((segment) => <i key={segment} className={segment <= value ? 'active' : ''} />)}</fieldset>;
}

const DEMO_TIME = new Date('2026-09-06T12:00:00Z').getTime();
export function Deadline({ date }: { date: string | null }) {
  if (!date) return <span className="deadline tone-neutral"><Clock3 size={17} />Unknown</span>;
  const days = Math.ceil((new Date(`${date}T12:00:00Z`).getTime() - DEMO_TIME) / 86_400_000);
  const tone = days <= 3 ? 'danger' : days <= 7 ? 'warning' : 'neutral';
  const label = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short' }).format(new Date(`${date}T12:00:00Z`));
  return <span className={`deadline tone-${tone}`}><Clock3 size={17} />{label}</span>;
}

export function EmptyState({ title, body, action }: { title: string; body: string; action?: { label: string; href: string } }) {
  return <section className="empty-state"><span>0</span><h2>{title}</h2><p>{body}</p>{action && <Link className="button primary" href={action.href}>{action.label}</Link>}</section>;
}

export function StatusBadge({ value }: { value: string }) {
  const lower = value.toLowerCase();
  const tone = lower.includes('complete') || lower.includes('offer') || lower.includes('confirmed') || lower.includes('interview') ? 'success' : lower.includes('partial') || lower.includes('review') || lower.includes('delayed') || lower.includes('likely') ? 'warning' : lower.includes('failed') || lower.includes('reject') || lower.includes('closed') ? 'danger' : 'neutral';
  return <span className={`status-badge ${tone}`}><i />{value}</span>;
}
