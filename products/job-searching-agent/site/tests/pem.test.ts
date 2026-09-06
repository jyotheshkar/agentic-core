import { describe, expect, it } from 'vitest';
import { pemBytes } from '@/lib/pem';

describe('PEM parsing', () => {
  it('strips constructed wrappers and whitespace without embedding key material', () => {
    const header = ['-----BEGIN', 'PRIVATE', 'KEY-----'].join(' ');
    const footer = ['-----END', 'PRIVATE', 'KEY-----'].join(' ');
    expect([...pemBytes(`${header}\nAQID\n${footer}`)]).toEqual([1, 2, 3]);
  });
});
