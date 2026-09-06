import { describe, expect, it } from 'vitest';
import { parseCsv } from '@/lib/csv';

describe('CSV audit import parsing', () => {
  it('handles quoted commas and CRLF', () => {
    const rows = parseCsv('company,role,city\r\n"Example, Ltd","AI Evaluator",London\r\n');
    expect(rows).toEqual([{ company: 'Example, Ltd', role: 'AI Evaluator', city: 'London' }]);
  });
  it('rejects duplicate headers', () => expect(() => parseCsv('company,company\nA,B')).toThrow(/duplicate/i));
  it('rejects unterminated quoted fields', () => expect(() => parseCsv('company,role\nA,"Broken')).toThrow(/unterminated/i));
});
