{{ config(materialized='view') }}

select
  order_id,
  payment_sequential,
  payment_type,
  safe_cast(payment_installments as int64) as payment_installments,
  safe_cast(payment_value as numeric)      as payment_value
from {{ source('olist_raw', 'olist_order_payments') }}
