export type ImportRow = Record<string, string>;

export function parseCsv(input: string): ImportRow[] {
  const rows: string[][] = [];
  let row: string[] = [], field = '', quoted = false;
  for (let index = 0; index < input.length; index++) {
    const char = input[index];
    if (quoted && char === '"' && input[index + 1] === '"') { field += '"'; index++; }
    else if (char === '"') quoted = !quoted;
    else if (!quoted && char === ',') { row.push(field); field = ''; }
    else if (!quoted && (char === '\n' || char === '\r')) { if (char === '\r' && input[index + 1] === '\n') index++; row.push(field); field = ''; if (row.some((value) => value.trim())) rows.push(row); row = []; }
    else field += char;
  }
  row.push(field); if (row.some((value) => value.trim())) rows.push(row);
  if (quoted) throw new Error('CSV contains an unterminated quoted field');
  const headers = rows.shift()?.map((value) => value.trim().toLowerCase()) ?? [];
  if (!headers.length || new Set(headers).size !== headers.length) throw new Error('CSV header is missing or contains duplicate columns');
  return rows.map((values) => Object.fromEntries(headers.map((header,index) => [header, values[index]?.trim() ?? ''])));
}
