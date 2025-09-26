select
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    UnitPrice,
    CustomerID,
    Country
from {{ ref('online_retail') }}
where CustomerID is not null
