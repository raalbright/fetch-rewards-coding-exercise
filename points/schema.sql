drop table if exists transactions;

create table transactions (
    payer text,
    points integer,
    timestamp datetime
);