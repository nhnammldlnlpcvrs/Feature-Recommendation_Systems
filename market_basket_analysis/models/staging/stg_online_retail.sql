select
    "InvoiceNo" as invoice_no,
    "StockCode" as stock_code,
    "Description" as description,
    "Quantity" as quantity,
    "InvoiceDate" as invoice_date,
    "UnitPrice" as unit_price,
    "CustomerID" as customer_id,
    "Country" as country
from {{ ref('online_retail') }}
