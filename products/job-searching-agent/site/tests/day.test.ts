import { describe, expect, it } from 'vitest';
import { investigationDay, investigationSubject } from '@/lib/day';

describe('continuous investigation day numbering', () => {
  it.each([
    ['2026-08-30T12:00:00Z', 30],
    ['2026-08-31T12:00:00Z', 31],
    ['2026-09-01T12:00:00Z', 32],
    ['2026-09-05T12:00:00Z', 36],
    ['2026-12-31T12:00:00Z', 153],
    ['2027-01-01T12:00:00Z', 154],
    ['2028-02-29T12:00:00Z', 578],
  ])('%s is Day %s', (iso, expected) => expect(investigationDay(new Date(iso))).toBe(expected));
  it('uses the exact email subject rule', () => expect(investigationSubject(new Date('2026-09-01T12:00:00Z'))).toBe('Day 32 Job Search Agent Investigation'));
  it('uses the London calendar through the autumn clock change', () => {
    expect(investigationDay(new Date('2026-10-25T00:30:00Z'))).toBe(86);
    expect(investigationDay(new Date('2026-10-26T00:30:00Z'))).toBe(87);
  });
});
