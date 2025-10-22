select
    "InvoiceNo"   as invoiceno,
    "StockCode"   as stockcode,
    "Description" as description,
    "Quantity"    as quantity,
    "InvoiceDate" as invoicedate,
    "UnitPrice"   as unitprice,
    "CustomerID"  as customerid,
    "Country"     as country
from {{ source('public', 'online_retail') }}