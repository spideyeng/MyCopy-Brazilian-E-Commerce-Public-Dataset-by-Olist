{{ config(materialized='table') }}

with dates as (
  select distinct
    date(order_purchase_timestamp) as date_day
  from {{ ref('stg_db_orders') }}
)

select
  date_day as date_key,
  extract(year from date_day)    as year,
  extract(quarter from date_day) as quarter,
  extract(month from date_day)   as month,
  extract(day from date_day)     as day,
  format_date('%Y-%m', date_day) as year_month
from dates

