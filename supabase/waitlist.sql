-- Waitlist for idealizepalace.com/waitlist (11 Nov 2026).
-- The site posts with the public anon key. Anon may INSERT only; nobody can read, change or delete rows
-- from the browser. Read the list in the Supabase dashboard (Table editor → waitlist) or with the service key.

create table if not exists public.waitlist (
  id          bigint generated always as identity primary key,
  email       text not null,
  source      text,
  created_at  timestamptz not null default now(),
  constraint waitlist_email_format check (
    char_length(email) between 6 and 254
    and email = lower(email)
    and email ~ '^[^\s@]+@[^\s@]+\.[^\s@]{2,}$'
  ),
  constraint waitlist_source_len check (source is null or char_length(source) <= 60)
);

create unique index if not exists waitlist_email_key on public.waitlist (email);

alter table public.waitlist enable row level security;

revoke all on public.waitlist from anon, authenticated;
grant insert (email, source) on public.waitlist to anon;

drop policy if exists "anyone can join the waitlist" on public.waitlist;
create policy "anyone can join the waitlist"
  on public.waitlist for insert to anon
  with check (true);
