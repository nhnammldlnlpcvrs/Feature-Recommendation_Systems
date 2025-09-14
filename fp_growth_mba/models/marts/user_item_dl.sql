{{ config(materialized='table') }}

with cleaned as (
    select *
    from {{ ref('stg_online_retail') }}
    where Quantity > 0 and UnitPrice > 0 and CustomerID is not null
      and not InvoiceNo like 'C%'
)

select distinct
    cast(CustomerID as integer) as user_id,
    lower(trim(Description))    as item_id
from cleaned
