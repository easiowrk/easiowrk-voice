create extension if not exists "pgcrypto";

-- Helpful indexes for common queries
create index if not exists idx_calls_agent_started
  on public.calls (agent_id, started_at desc);

create index if not exists idx_calls_status_started
  on public.calls (status, started_at desc);
