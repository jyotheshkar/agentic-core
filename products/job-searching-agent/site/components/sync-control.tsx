'use client';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { AlertCircle, Check, RefreshCw } from 'lucide-react';
import { useEffect, useRef } from 'react';

export function SyncControl({ automatic = false }: { automatic?: boolean }) {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: async () => { const response = await fetch('/api/sync/google-sheets', { method: 'POST' }); const body = await response.json() as { detail?: string; error?: string }; if (!response.ok) throw new Error(body.detail ?? body.error ?? 'Sync failed'); return body; },
    onSuccess: () => queryClient.invalidateQueries(),
  });
  const mutate = mutation.mutate;
  const started = useRef(false);
  useEffect(() => { if (!automatic || started.current) return; started.current = true; mutate(); const timer = window.setInterval(() => mutate(), 60_000); return () => window.clearInterval(timer); }, [automatic, mutate]);
  const label = mutation.isPending ? 'Syncing' : mutation.isSuccess ? 'Synced' : mutation.isError ? 'Needs setup' : 'Refresh';
  return <button className="button secondary" onClick={() => mutation.mutate()} title={mutation.error?.message} aria-label={`Google Sheets sync: ${label}`}>{mutation.isPending ? <RefreshCw className="spin" size={17} /> : mutation.isSuccess ? <Check size={17} /> : mutation.isError ? <AlertCircle size={17} /> : <RefreshCw size={17} />}{label}</button>;
}
