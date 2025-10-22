{{ config(materialized='table') }}

with raw as (
    select
        invoiceno as transaction_id,
        lower(trim(description)) as item_name
    from {{ ref('stg_online_retail') }}
    where quantity > 0 and description is not null
)

select
    transaction_id,
    string_agg(item_name, ',') as items
from raw
group by transaction_id