select
    {{ dbt_utils.generate_surrogate_key(['vendor', 'chip_name', 'year']) }} as chip_year_key,
    chip_name,
    vendor,
    launch_date,
    year,
    memory_gb,
    fp16_tflops,
    tdp_watts,
    estimated_shipments_units,
    estimated_asp_usd,
    estimated_revenue_usd_m,
    estimated_revenue_usd_m * 1000000 as estimated_revenue_usd,
    description
from {{ ref('stg_ai_chip_market') }}
