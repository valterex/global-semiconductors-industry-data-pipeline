{{
    config(materialized="view")
}}

select
    d.vendor,
    s.year,
    sum(s.estimated_revenue_usd_m) as estimated_revenue_usd_m
from {{ ref('fct_ai_chip_sales') }} s
join {{ ref('dim_ai_chips') }} d on s.chip_key = d.chip_key
group by d.vendor, s.year
