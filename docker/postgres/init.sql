CREATE SCHEMA IF NOT EXISTS budget;
DROP VIEW IF EXISTS budget.vista;

CREATE OR REPLACE VIEW budget.vista AS
    SELECT 'доход' as type, i.id, i.value, i.operation_date, i.bank_account_id, c.name as comment
    FROM budget_income i
    JOIN budget_incomesubcategory c ON c.id = i.sub_category_id
    WHERE i.deleted_at is null
  UNION ALL
    SELECT 'расход' as type, e.id, -1 * e.value, e.operation_date, e.bank_account_id, c.name as comment
    FROM budget_expenditure e
    JOIN budget_expendituresubcategory c ON c.id = e.sub_category_id
    WHERE e.deleted_at is null
  UNION ALL
    SELECT 'перевод' as type, t.id, -1* t.value, t.operation_date, t.bank_account_id, a.name as comment
    FROM budget_transfer t
    JOIN budget_bankaccount a ON a.id = t.bank_account_id
    WHERE t.deleted_at is null
  UNION ALL
    SELECT 'перевод' as type, t.id, t.value, t.operation_date, t.bank_account_to_id, a.name as comment
    FROM budget_transfer t
    JOIN budget_bankaccount a ON a.id = t.bank_account_to_id
    WHERE t.deleted_at is null;