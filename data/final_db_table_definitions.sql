CREATE TABLE IF NOT EXISTS public.categories (
	category_id int2 NOT NULL,
	category_name varchar(15) NOT NULL,
	description text,
	picture bytea
);

CREATE TABLE IF NOT EXISTS public.customer_customer_demo (
	customer_id bpchar NOT NULL,
	customer_type_id bpchar NOT NULL
);

CREATE TABLE IF NOT EXISTS public.customer_demographics (
	customer_type_id bpchar NOT NULL,
	customer_desc text
);

CREATE TABLE IF NOT EXISTS public.customers (
	customer_id bpchar NOT NULL,
	company_name varchar(40) NOT NULL,
	contact_name varchar(30),
	contact_title varchar(30),
	address varchar(60),
	city varchar(15),
	region varchar(15),
	postal_code varchar(10),
	country varchar(15),
	phone varchar(24),
	fax varchar(24)
);

CREATE TABLE IF NOT EXISTS public.employee_territories (
	employee_id int2 NOT NULL,
	territory_id varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.employees (
	employee_id int2 NOT NULL,
	last_name varchar(20) NOT NULL,
	first_name varchar(10) NOT NULL,
	title varchar(30),
	title_of_courtesy varchar(25),
	birth_date date,
	hire_date date,
	address varchar(60),
	city varchar(15),
	region varchar(15),
	postal_code varchar(10),
	country varchar(15),
	home_phone varchar(24),
	"extension" varchar(4),
	photo bytea,
	notes text,
	reports_to int2,
	photo_path varchar(255)
);

CREATE TABLE IF NOT EXISTS public.orders (
	order_id int2 NOT NULL,
	customer_id bpchar,
	employee_id int2,
	order_date date,
	required_date date,
	shipped_date date,
	ship_via int2,
	freight float4,
	ship_name varchar(40),
	ship_address varchar(60),
	ship_city varchar(15),
	ship_region varchar(15),
	ship_postal_code varchar(10),
	ship_country varchar(15)
);

CREATE TABLE IF NOT EXISTS public.region (
	region_id int2 NOT NULL,
	region_description bpchar NOT NULL
);

CREATE TABLE IF NOT EXISTS public.shippers (
	shipper_id int2 NOT NULL,
	company_name varchar(40) NOT NULL,
	phone varchar(24) NULL
);

CREATE TABLE IF NOT EXISTS public.suppliers (
	supplier_id int2 NOT NULL,
	company_name varchar(40) NOT NULL,
	contact_name varchar(30) NULL,
	contact_title varchar(30) NULL,
	address varchar(60) NULL,
	city varchar(15) NULL,
	region varchar(15) NULL,
	postal_code varchar(10) NULL,
	country varchar(15) NULL,
	phone varchar(24) NULL,
	fax varchar(24) NULL,
	homepage text NULL
);

CREATE TABLE IF NOT EXISTS public.us_states (
	state_id int2 NOT NULL,
	state_name varchar(100) NULL,
	state_abbr varchar(2) NULL,
	state_region varchar(50) NULL
);

CREATE TABLE IF NOT EXISTS public.territories (
	territory_id varchar(20) NOT NULL,
	territory_description bpchar NOT NULL,
	region_id int2 NOT NULL
);

CREATE TABLE IF NOT EXISTS public.products (
	product_id int2 NOT NULL,
	product_name varchar(40) NOT NULL,
	supplier_id int2 NULL,
	category_id int2 NULL,
	quantity_per_unit varchar(20) NULL,
	unit_price float4 NULL,
	units_in_stock int2 NULL,
	units_on_order int2 NULL,
	reorder_level int2 NULL,
	discontinued int4 NOT NULL
);