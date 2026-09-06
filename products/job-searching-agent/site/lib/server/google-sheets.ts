import type { ImportRow } from '@/lib/csv';
import { pemBytes } from '@/lib/pem';
import { runtimeEnv } from './runtime';

function base64Url(value: string | Uint8Array) {
  const bytes = typeof value === 'string' ? new TextEncoder().encode(value) : value;
  const binary = String.fromCharCode(...bytes);
  return btoa(binary).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');
}

async function accessToken(email: string, privateKey: string) {
  const now = Math.floor(Date.now() / 1000);
  const header = base64Url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claim = base64Url(JSON.stringify({ iss: email, scope: 'https://www.googleapis.com/auth/spreadsheets.readonly', aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600 }));
  const key = await crypto.subtle.importKey('pkcs8', pemBytes(privateKey.replaceAll('\\n','\n')), { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
  const signature = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(`${header}.${claim}`));
  const assertion = `${header}.${claim}.${base64Url(new Uint8Array(signature))}`;
  const response = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion }), signal: AbortSignal.timeout(15_000) });
  if (!response.ok) throw new Error(`Google authentication failed with status ${response.status}`);
  const data = await response.json<{ access_token?: string }>();
  if (!data.access_token) throw new Error('Google authentication returned no access token');
  return data.access_token;
}

export async function readJobRows(): Promise<ImportRow[]> {
  const env = runtimeEnv();
  const sheetId = env.GOOGLE_SHEET_ID;
  const email = env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKey = env.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY;
  const worksheet = env.GOOGLE_WORKSHEET_JOBS ?? 'Daily Job List';
  if (!sheetId || !email || !privateKey) throw new Error('NEEDS REVIEW: Google Sheets credentials are not configured');
  const token = await accessToken(email, privateKey);
  const range = encodeURIComponent(`'${worksheet}'!A:Z`);
  const response = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${encodeURIComponent(sheetId)}/values/${range}?majorDimension=ROWS`, { headers: { authorization: `Bearer ${token}` }, signal: AbortSignal.timeout(20_000) });
  if (!response.ok) throw new Error(`Google Sheets read failed with status ${response.status}`);
  const data = await response.json<{ values?: unknown[][] }>();
  const [headerRow, ...rows] = data.values ?? [];
  if (!headerRow) return [];
  const headers = headerRow.map((value) => String(value).trim().toLowerCase());
  const cell = (value: unknown) => typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean' ? String(value).trim() : value == null ? '' : JSON.stringify(value);
  return rows.filter((row) => row.some((value) => cell(value))).map((row) => Object.fromEntries(headers.map((header,index) => [header, cell(row[index])])));
}
