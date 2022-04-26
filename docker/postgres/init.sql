CREATE SCHEMA IF NOT EXISTS budget;
DROP VIEW IF EXISTS budget.history;

create view history(type, id, value, operation_date, bank_account_id, comment) as
SELECT 'доход'::text AS type,
       i.id,
       i.value,
       i.operation_date,
       i.bank_account_id,
       c.name        AS comment
FROM budget_income i
         JOIN budget_incomesubcategory c ON c.id = i.sub_category_id
WHERE i.deleted_at IS NULL
UNION ALL
SELECT 'расход'::text                   AS type,
       e.id,
       '-1'::integer::numeric * e.value AS value,
       e.operation_date,
       e.bank_account_id,
       c.name                           AS comment
FROM budget_expenditure e
         JOIN budget_expendituresubcategory c ON c.id = e.sub_category_id
WHERE e.deleted_at IS NULL
UNION ALL
SELECT 'перевод'::text                  AS type,
       t.id,
       '-1'::integer::numeric * t.value AS value,
       t.operation_date,
       t.bank_account_id,
       a.name                           AS comment
FROM budget_transfer t
         JOIN budget_bankaccount a ON a.id = t.bank_account_id
WHERE t.deleted_at IS NULL
UNION ALL
SELECT 'перевод'::text      AS type,
       t.id,
       t.value,
       t.operation_date,
       t.bank_account_to_id AS bank_account_id,
       a.name               AS comment
FROM budget_transfer t
         JOIN budget_bankaccount a ON a.id = t.bank_account_to_id
WHERE t.deleted_at IS NULL;