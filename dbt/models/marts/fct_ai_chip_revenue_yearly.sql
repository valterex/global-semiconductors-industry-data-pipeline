{{
    config(materialized="view")
}}

select
    vendor,
    year,
    sum(estimated_revenue_usd_m) as revenue_usd_m
from {{ ref('fct_ai_chip_market') }}
group by vendor, year
