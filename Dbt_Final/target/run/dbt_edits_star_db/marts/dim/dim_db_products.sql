
  
    

    create or replace table `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_products`
      
    
    

    OPTIONS()
    as (
      

with products as (
  select
    product_id,
    product_category_name,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
  from `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_products`
),
cats as (
  select
    product_category_name,
    product_category_name_english
  from `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_product_category_name_translation`
)

select
  p.product_id,
  p.product_category_name,
  c.product_category_name_english,
  p.product_weight_g,
  p.product_length_cm,
  p.product_height_cm,
  p.product_width_cm
from products p
left join cats c
    on p.product_category_name = c.product_category_name
    );
  