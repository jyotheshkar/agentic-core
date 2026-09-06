import { findJob } from '@/lib/server/repository';
import { json } from '@/lib/server/runtime';
export async function GET(_request: Request, context: { params: Promise<{ id: string }> }) { const { id } = await context.params; const result = await findJob(id); return result.record ? json(result) : json({ error: 'Job not found' }, { status: 404 }); }
