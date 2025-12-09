

select
  order_id,
  order_item_id,
  product_id,
  seller_id,
  safe_cast(price as numeric)         as price,
  safe_cast(freight_value as numeric) as freight_value
from `durable-ripsaw-477914-g0`.`ecommerce`.`olist_order_items`