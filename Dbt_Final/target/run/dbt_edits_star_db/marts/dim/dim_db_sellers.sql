
  
    

    create or replace table `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_sellers`
      
    
    

    OPTIONS()
    as (
      

select
  seller_id,
  seller_zip_code_prefix as seller_zip,
  seller_city,
  seller_state
from `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_sellers`
    );
  