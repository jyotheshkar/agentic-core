import { applicationTimeline } from '@/lib/server/repository';
import { json, requireOwner } from '@/lib/server/runtime';

export async function GET(request: Request, context: { params: Promise<{ id: string }> }) {
  requireOwner(request);
  const { id } = await context.params;
  return json(await applicationTimeline(id));
}
