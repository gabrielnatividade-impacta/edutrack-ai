table subjects {
  id uuid primary_key,
  name text,
  code text?,
  description text?,
  status text default="active",
  user_id uuid references=users.id,
  account_id uuid? references=accounts.id,
  created_at timestamp default=now(),
  updated_at timestamp default=now()
}