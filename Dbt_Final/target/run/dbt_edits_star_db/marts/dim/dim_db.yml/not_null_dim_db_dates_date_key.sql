
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_key
from `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_dates`
where date_key is null



  
  
      
    ) dbt_internal_test