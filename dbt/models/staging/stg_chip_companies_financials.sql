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
    capex_usd_bn
from {{ source('raw', 'chip_companies_financials') }}
where year is not null
