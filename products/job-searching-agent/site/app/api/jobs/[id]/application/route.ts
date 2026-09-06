import { ZodError } from 'zod';
import { applicationUpdateSchema, updateApplication } from '@/lib/server/application';
import { json, requireOwner } from '@/lib/server/runtime';
export async function PATCH(request: Request, context: { params: Promise<{ id: string }> }) {
  try { const actor = requireOwner(request); const { id } = await context.params; const input = applicationUpdateSchema.parse(await request.json()); return json(await updateApplication(id, actor, input)); }
  catch (error) { if (error instanceof Response) return error; if (error instanceof ZodError) return json({ error: 'Invalid application update', issues: error.issues }, { status: 400 }); return json({ error: 'Application update failed', detail: error instanceof Error ? error.message : 'Unknown error' }, { status: 500 }); }
}
