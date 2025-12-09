

select
  oi.order_id,
  oi.order_item_id,
  oi.product_id,
  oi.seller_id,
  o.customer_id,
  date(o.order_purchase_timestamp) as order_date_key,
  oi.price,
  oi.freight_value,
  (oi.price + oi.freight_value) as gross_order_item_value
from `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_order_items` oi
left join `durable-ripsaw-477914-g0`.`ecommerce`.`stg_db_orders` o
  on oi.order_id = o.order_id