select
    year_month,
    year,
    product,
    currency,
    unit,
    price,
    case when currency = 'USD' then price end as price_usd
from {{ ref('stg_chip_prices') }}
