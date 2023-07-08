select 
	orders.order_id,
	products.product_name,
	orders.order_date,
	orders.shipped_date,
	orders.required_date,
	order_details.unit_price,
	order_details.quantity,
	order_details.discount
from 
	public.order_details as order_details,
	public.orders as orders,
	public.products as products
where
    order_details.order_id = orders.order_id
	and order_details.product_id = products.product_id;