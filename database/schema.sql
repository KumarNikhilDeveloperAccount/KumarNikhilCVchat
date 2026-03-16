create extension if not exists "pgcrypto";

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  display_name text,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  status text not null default 'active'
);

create table if not exists profiles (
  user_id uuid primary key references users(id) on delete cascade,
  bio text,
  locale text default 'en-IN',
  timezone text default 'Asia/Calcutta',
  preferred_tone text default 'balanced',
  preferred_theme text default 'elegant',
  kid_mode_enabled boolean not null default false,
  accessibility_prefs jsonb not null default '{}'::jsonb,
  device_prefs jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists conversations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  title text,
  platform text not null,
  last_message_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references conversations(id) on delete cascade,
  sender_type text not null check (sender_type in ('user', 'assistant', 'system')),
  model_used text,
  prompt_tokens int default 0,
  completion_tokens int default 0,
  content text not null,
  structured_payload jsonb,
  safety_flags jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists user_preferences (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  pref_key text not null,
  pref_value jsonb not null,
  confidence numeric(4,3) not null default 0.800,
  source text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, pref_key)
);

create table if not exists memory_entries (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  memory_type text not null,
  summary text not null,
  source_message_id uuid references messages(id) on delete set null,
  source_kind text not null,
  trust_score numeric(4,3) not null default 0.700,
  sensitivity text not null default 'normal',
  is_active boolean not null default true,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists memory_chunks (
  id uuid primary key default gen_random_uuid(),
  memory_entry_id uuid not null references memory_entries(id) on delete cascade,
  chunk_index int not null,
  content text not null,
  token_count int not null,
  embedding_ref text,
  created_at timestamptz not null default now(),
  unique (memory_entry_id, chunk_index)
);

create table if not exists theme_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  theme_id text not null,
  theme_tokens jsonb not null,
  generated_by text not null default 'system',
  is_active boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete set null,
  session_id text,
  event_type text not null,
  event_payload jsonb not null default '{}'::jsonb,
  source_service text not null,
  created_at timestamptz not null default now()
);

create table if not exists api_usage (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete set null,
  provider text not null,
  model text not null,
  request_count int not null default 1,
  prompt_tokens int not null default 0,
  completion_tokens int not null default 0,
  estimated_cost_usd numeric(10,6) not null default 0,
  created_at timestamptz not null default now()
);

