{{ config(materialized='view') }}

select
  product_category_name,
  product_category_name_english
from {{ source('olist_raw', 'product_category_name_translation') }}
