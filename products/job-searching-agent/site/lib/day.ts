const BASE_DATE = { year: 2026, month: 8, day: 30 };

function londonParts(date: Date) {
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', year: 'numeric', month: 'numeric', day: 'numeric' }).formatToParts(date);
  const value = (type: string) => Number(parts.find((part) => part.type === type)?.value);
  return { year: value('year'), month: value('month'), day: value('day') };
}

export function investigationDay(date = new Date()) {
  const current = londonParts(date);
  const baseUtc = Date.UTC(BASE_DATE.year, BASE_DATE.month - 1, BASE_DATE.day);
  const currentUtc = Date.UTC(current.year, current.month - 1, current.day);
  return 30 + Math.floor((currentUtc - baseUtc) / 86_400_000);
}

export function londonDateLabel(date = new Date()) {
  return new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', day: 'numeric', month: 'short', year: 'numeric' }).format(date).toUpperCase();
}

export function investigationSubject(date = new Date()) {
  return `Day ${investigationDay(date)} Job Search Agent Investigation`;
}
