{{ config(materialized='view') }}

select
  order_id,
  customer_id,
  order_status,
  safe_cast(order_purchase_timestamp as timestamp)    as order_purchase_timestamp,
  safe_cast(order_approved_at as timestamp)           as order_approved_at,
  safe_cast(order_delivered_carrier_date as timestamp) as order_delivered_carrier_date,
  safe_cast(order_delivered_customer_date as timestamp) as order_delivered_customer_date,
  safe_cast(order_estimated_delivery_date as timestamp) as order_estimated_delivery_date
from {{ source('olist_raw', 'olist_orders') }}

