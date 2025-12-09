
  
    

    create or replace table `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_customers`
      
    
    

    OPTIONS()
    as (
      

select
  customer_id,
  customer_unique_id,
  customer_zip_code_prefix,
  customer_city,
  customer_state
from `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_customers`
    );
  