import { env } from 'cloudflare:workers';

export type RuntimeEnv = Cloudflare.Env & {
  GOOGLE_SHEET_ID?: string;
  GOOGLE_SERVICE_ACCOUNT_EMAIL?: string;
  GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY?: string;
  GOOGLE_WORKSHEET_JOBS?: string;
};

export function runtimeEnv() { return env as RuntimeEnv; }

export function actorFromRequest(request: Request) {
  const actor = request.headers.get('oai-authenticated-user-id') ?? request.headers.get('x-openai-user-id');
  if (actor) return actor;
  if (process.env.NODE_ENV !== 'production') return 'local-owner';
  return null;
}

export function requireOwner(request: Request) {
  const actor = actorFromRequest(request);
  if (!actor) throw new Response(JSON.stringify({ error: 'Owner authentication required' }), { status: 401, headers: { 'content-type': 'application/json' } });
  return actor;
}

export function json(data: unknown, init: ResponseInit = {}) {
  const headers = new Headers(init.headers);
  headers.set('cache-control', 'no-store');
  return Response.json(data, { ...init, headers });
}

export function id(prefix: string) { return `${prefix}_${crypto.randomUUID()}`; }
