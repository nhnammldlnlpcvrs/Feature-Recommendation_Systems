
  
    

  create  table "fp_growth_mba"."public"."transaction_fpgrowth__dbt_tmp"
  
  
    as
  
  (
    

with raw as (
    select
        invoiceno as transaction_id,
        lower(trim(description)) as item_name
    from "fp_growth_mba"."public"."stg_online_retail"
    where quantity > 0 and description is not null
)

select
    transaction_id,
    string_agg(item_name, ',') as items
from raw
group by transaction_id
  );
  