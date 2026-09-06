'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart3, BriefcaseBusiness, CalendarDays, CircleGauge, FileText, ListTodo, Menu, Settings, X } from 'lucide-react';
import { useState } from 'react';

const nav = [
  { label: 'Overview', href: '/', icon: CircleGauge },
  { label: 'All Jobs', href: '/jobs', icon: BriefcaseBusiness },
  { label: 'Application Queue', href: '/queue', icon: ListTodo },
  { label: 'Applications', href: '/applications', icon: FileText },
  { label: 'Daily Investigations', href: '/investigations', icon: CalendarDays },
  { label: 'Agent Performance', href: '/performance', icon: BarChart3 },
  { label: 'Settings', href: '/settings', icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [moreOpen, setMoreOpen] = useState(false);
  const isActive = (href: string) => href === '/' ? pathname === '/' : pathname.startsWith(href);
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="wordmark" href="/">JOB SEARCHING AGENT</Link>
        <nav aria-label="Primary navigation">
          {nav.map(({ label, href, icon: Icon }) => <Link href={href} className={isActive(href) ? 'nav-link active' : 'nav-link'} key={label}><Icon size={20} strokeWidth={1.8} /><span>{label}</span></Link>)}
        </nav>
        <span className="version">V 3.0</span>
      </aside>
      <main className="workspace">{children}</main>
      <nav className="mobile-nav" aria-label="Mobile navigation">
        {nav.slice(0, 4).map(({ label, href, icon: Icon }) => <Link key={label} href={href} className={isActive(href) ? 'active' : ''}><Icon size={19} /><span>{label === 'Application Queue' ? 'Queue' : label}</span></Link>)}
        <button type="button" className={moreOpen ? 'active' : ''} onClick={() => setMoreOpen(true)}><Menu size={19} /><span>More</span></button>
      </nav>
      {moreOpen && <div className="more-backdrop"><dialog open className="more-sheet" aria-label="More navigation"><header><strong>More</strong><button aria-label="Close menu" onClick={() => setMoreOpen(false)}><X /></button></header>{nav.slice(4).map(({ label, href, icon: Icon }) => <Link key={label} href={href} onClick={() => setMoreOpen(false)}><Icon size={20} />{label}</Link>)}<footer>Job Searching Agent <strong>V 3.0</strong></footer></dialog></div>}
    </div>
  );
}
