select
    year_month,
    year,
    product,
    currency,
    unit,
    price
from {{ source('raw', 'chip_prices') }}
where year is not null
