
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select seller_id
from `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_sellers`
where seller_id is null



  
  
      
    ) dbt_internal_test