export function pemBytes(pem: string) {
  const pemHeader = ['-----BEGIN', 'PRIVATE', 'KEY-----'].join(' ');
  const pemFooter = ['-----END', 'PRIVATE', 'KEY-----'].join(' ');
  const body = pem.replaceAll(pemHeader, '').replaceAll(pemFooter, '').replace(/\s/g,'');
  const binary = atob(body);
  return Uint8Array.from(binary, (char) => char.charCodeAt(0));
}
