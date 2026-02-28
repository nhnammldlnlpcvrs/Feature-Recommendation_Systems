
  create view "fp_growth_mba"."public"."stg_online_retail__dbt_tmp"
    
    
  as (
    select
    "InvoiceNo"   as invoiceno,
    "StockCode"   as stockcode,
    "Description" as description,
    "Quantity"    as quantity,
    "InvoiceDate" as invoicedate,
    "UnitPrice"   as unitprice,
    "CustomerID"  as customerid,
    "Country"     as country
from "fp_growth_mba"."public"."online_retail"
  );