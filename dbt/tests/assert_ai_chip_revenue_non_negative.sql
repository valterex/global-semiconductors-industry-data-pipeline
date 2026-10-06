select
    chip_year_key
from {{ ref('fct_ai_chip_sales') }}
where estimated_revenue_usd_m < 0
