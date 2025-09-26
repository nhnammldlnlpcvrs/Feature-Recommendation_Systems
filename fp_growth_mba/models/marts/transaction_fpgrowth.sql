{{ config(materialized='table') }}

with raw as (
    select
        InvoiceNo as transaction_id,
        lower(trim(Description)) as item_name
    from {{ ref('stg_online_retail') }}
    where Quantity > 0 and Description is not null
)

select
    transaction_id,
    group_concat(item_name, ',') as items
from raw
group by transaction_id
