create table if not exists public.users (
    user_id text primary key,
    email text not null unique,
    password text not null,
    name text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- 기존 bigint identity 컬럼이 있으면 데이터를 유지한 채 문자열 ID 컬럼으로 변경합니다.
alter table public.users alter column user_id drop identity if exists;
alter table public.users alter column user_id type text using user_id::text;

create or replace function public.set_users_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists users_set_updated_at on public.users;

create trigger users_set_updated_at
before update on public.users
for each row
execute function public.set_users_updated_at();

-- 개발 확인용 임시 회원입니다. 운영 환경에서는 아래 INSERT 구문을 제외하세요.
-- 모든 비밀번호는 평문이 아닌 PBKDF2-SHA256 해시로 저장합니다.
insert into public.users (user_id, email, password, name)
values
    ('20260722235959001', 'temp-user-01@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원01'),
    ('20260722235959002', 'temp-user-02@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원02'),
    ('20260722235959003', 'temp-user-03@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원03'),
    ('20260722235959004', 'temp-user-04@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원04'),
    ('20260722235959005', 'temp-user-05@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원05'),
    ('20260722235959006', 'temp-user-06@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원06'),
    ('20260722235959007', 'temp-user-07@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원07'),
    ('20260722235959008', 'temp-user-08@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원08'),
    ('20260722235959009', 'temp-user-09@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원09'),
    ('20260722235959010', 'temp-user-10@example.com', 'pbkdf2_sha256$600000$4raNjbxK9dGMvwIVYYgTog==$P7zvKA+cTEGhZnk3h9Dzj4ev/TCM0CuBc5bZDn6sUfE=', '임시회원10')
on conflict do nothing;
