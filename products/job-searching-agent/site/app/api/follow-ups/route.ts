import { manualFollowUps } from '@/lib/server/repository';
import { json, requireOwner } from '@/lib/server/runtime';

export async function GET(request: Request) {
  requireOwner(request);
  return json(await manualFollowUps());
}
