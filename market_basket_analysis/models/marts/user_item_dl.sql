{{ config(materialized='table') }}

with cleaned as (
    select *
    from {{ ref('stg_online_retail') }}
    where quantity > 0 
      and unit_price > 0 
      and customer_id is not null
      and not invoice_no like 'C%'
)

select distinct
    cast(customer_id as integer) as user_id,
    lower(trim(description))     as item_id
from cleaned
