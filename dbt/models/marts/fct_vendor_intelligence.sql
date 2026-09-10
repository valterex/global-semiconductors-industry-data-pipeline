with vendor_revenue as (
    select
        lower(trim(vendor)) as vendor_name,
        vendor as vendor_display,
        year,
        sum(estimated_revenue_usd_m) as ai_chip_revenue_usd_m
    from {{ ref('fct_ai_chip_market') }}
    group by 1, 2, 3
),

company_financials as (
    select
        lower(trim(company_name)) as company_name,
        company_name as company_display,
        year,
        sum(revenue_usd_bn) as company_revenue_usd_bn,
        avg(rd_intensity_pct) as rd_intensity_pct
    from {{ ref('fct_company_financials') }}
    group by 1, 2, 3
),

fab_capacity as (
    select
        lower(trim(company)) as company_name,
        company as company_display,
        year,
        sum(annual_wafer_capacity) as annual_wafer_capacity
    from {{ ref('fct_fab_capacity') }}
    group by 1, 2, 3
)

select
    {{ dbt_utils.generate_surrogate_key(['vr.vendor_name', 'vr.year']) }} as vendor_year_key,
    vr.vendor_display as vendor,
    vr.year,
    vr.ai_chip_revenue_usd_m,
    cf.company_revenue_usd_bn,
    cf.rd_intensity_pct,
    fc.annual_wafer_capacity
from vendor_revenue as vr
left join company_financials as cf
    on vr.vendor_name = cf.company_name
    and vr.year = cf.year
left join fab_capacity as fc
    on vr.vendor_name = fc.company_name
    and vr.year = fc.year
