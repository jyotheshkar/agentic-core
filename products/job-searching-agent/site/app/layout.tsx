import type { Metadata } from 'next';
import { Inter, Roboto_Condensed } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/providers';
import { WebMcpBridge } from '@/components/webmcp-bridge';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });
const condensed = Roboto_Condensed({ variable: '--font-condensed', subsets: ['latin'] });

export const metadata: Metadata = { title: 'Job Searching Agent', description: 'Private UK job search operations dashboard' };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className={`${inter.variable} ${condensed.variable}`}><Providers>{children}<WebMcpBridge /></Providers></body></html>;
}
