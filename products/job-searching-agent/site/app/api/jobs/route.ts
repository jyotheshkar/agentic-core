import { listJobs } from '@/lib/server/repository';
import { json } from '@/lib/server/runtime';
export async function GET(request: Request) {
  const { records, source } = await listJobs();
  const url = new URL(request.url);
  const status = url.searchParams.get('status');
  const country = url.searchParams.get('country');
  const query = url.searchParams.get('q')?.toLowerCase();
  const filtered = records.filter((job) => (!status || job.status === status) && (!country || job.country === country) && (!query || `${job.company} ${job.role} ${job.city} ${job.recommendationId}`.toLowerCase().includes(query)));
  return json({ source, count: filtered.length, records: filtered });
}
