select
    year,
    company_name,
    ticker,
    country_iso3,
    segment,
    revenue_usd_bn,
    operating_margin_pct,
    operating_income_usd_bn,
    rd_spend_usd_bn,
    rd_spend_usd_bn / nullif(revenue_usd_bn, 0) * 100 as rd_intensity_pct,
    capex_usd_bn
from {{ ref('stg_chip_companies_financials') }}
