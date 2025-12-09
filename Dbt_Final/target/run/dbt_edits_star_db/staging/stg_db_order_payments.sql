

  create or replace view `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_order_payments`
  OPTIONS()
  as 

select
  order_id,
  payment_sequential,
  payment_type,
  safe_cast(payment_installments as int64) as payment_installments,
  safe_cast(payment_value as numeric)      as payment_value
from `durable-ripsaw-477914-g0`.`ecommerce`.`olist_order_payments`;

