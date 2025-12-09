{{ config(materialized='table') }}

select
  seller_id,
  seller_zip_code_prefix as seller_zip,
  seller_city,
  seller_state
from {{ ref('stg_db_sellers') }}



