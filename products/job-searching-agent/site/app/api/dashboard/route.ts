import { dashboardData } from '@/lib/server/repository';
import { json } from '@/lib/server/runtime';
export async function GET() { return json(await dashboardData()); }
