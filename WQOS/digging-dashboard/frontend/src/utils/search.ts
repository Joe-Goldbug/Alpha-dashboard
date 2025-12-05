import { ConfigTemplate } from '../types/config';

export const splitTokens = (q: string): string[] => {
  return (q || '')
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean);
};

export const matchByTokens = (tokens: string[], searchable: string): boolean => {
  if (!tokens.length) return true;
  const s = (searchable || '').toLowerCase();
  return tokens.every((t) => s.includes(t));
};

export const buildSearchableFromTemplate = (t: ConfigTemplate): string => {
  const c = (t as any).config_data || {};
  const parts = [
    t.name || '',
    t.description || '',
    c.region || '',
    c.universe || '',
    `delay:${c.delay ?? ''}`,
  ];
  return parts.join(' ').toLowerCase();
};

export const buildSearchableFromScript = (s: {
  script_name?: string;
  tag?: string;
  status?: string;
  pid?: number;
}): string => {
  const stage = s.tag ? (s.tag.split('_').pop() ?? '') : '';
  const parts = [
    s.script_name || '',
    s.tag || '',
    s.status || '',
    String(s.pid ?? ''),
    stage,
  ];
  return parts.join(' ').toLowerCase();
};

