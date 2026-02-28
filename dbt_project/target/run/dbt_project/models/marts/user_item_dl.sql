
  
    

  create  table "fp_growth_mba"."public"."user_item_dl__dbt_tmp"
  
  
    as
  
  (
    

with cleaned as (
    select *
    from "fp_growth_mba"."public"."stg_online_retail"
    where quantity > 0 
      and unitprice > 0 
      and customerid is not null
      and not invoiceno like 'C%'
)

select distinct
    cast(customerid as integer) as user_id,
    lower(trim(description))    as item_id
from cleaned
  );
  