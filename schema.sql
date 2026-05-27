
create table if not exists employees (
    id bigserial primary key,
    employee_code text unique,
    full_name text not null,
    leader_name text,
    route text,
    is_active boolean default true,
    created_at timestamptz default now()
);

create table if not exists products (
    code text primary key,
    name text not null,
    price numeric default 0,
    product_group text default 'OTHER',
    active boolean default true,
    updated_at timestamptz default now()
);

create table if not exists pn_prices (
    code text primary key,
    name text not null,
    price numeric not null,
    active boolean default true,
    coefficient numeric default 1,
    channel text default 'RETAIL',
    updated_at timestamptz default now()
);

create table if not exists opening_balances (
    id bigserial primary key,
    employee_name text not null,
    balance_date date,
    data jsonb not null default '{}'::jsonb,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists sales_reports (
    id text primary key,
    report_date date not null,
    employee_name text not null,
    leader_name text,
    route text,
    opening jsonb not null default '{}'::jsonb,
    transactions jsonb not null default '{}'::jsonb,
    pn_sales jsonb not null default '{}'::jsonb,
    paid numeric default 0,
    status text default 'SUBMITTED',
    raw_data jsonb not null default '{}'::jsonb,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists audit_logs (
    id bigserial primary key,
    table_name text,
    record_id text,
    action text,
    old_data jsonb,
    new_data jsonb,
    actor text,
    created_at timestamptz default now()
);

create index if not exists idx_sales_reports_date_employee on sales_reports(report_date, employee_name);
create index if not exists idx_opening_employee on opening_balances(employee_name);

insert into pn_prices(code, name, price, coefficient, channel)
values
('PN75','Phân nước giá 75',75000,0.7,'DEALER'),
('PN80','Phân nước giá 80',80000,0.7,'DEALER'),
('PN83','Phân nước giá 83',83000,0.7,'DEALER'),
('PN90','Phân nước giá 90',90000,0.7,'DEALER'),
('PN95','Phân nước giá 95',95000,0.7,'DEALER'),
('PN100','Phân nước bán lẻ 100',100000,1.0,'RETAIL')
on conflict (code) do nothing;
