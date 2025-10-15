select
    invoiceno,
    stockcode,
    description,
    quantity,
    invoicedate,
    unitprice,
    customerid,
    "Country" as country
from {{ source('public', 'online_retail') }}