

  create or replace view `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_product_category_name_translation`
  OPTIONS()
  as 

select
  product_category_name,
  product_category_name_english
from `durable-ripsaw-477914-g0`.`ecommerce`.`product_category_name_translation`;

