
    
    

with dbt_test__target as (

  select date_key as unique_field
  from `durable-ripsaw-477914-g0`.`ecommerce`.`dim_db_dates`
  where date_key is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


