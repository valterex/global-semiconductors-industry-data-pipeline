select
    year,
    chip_name,
    vendor,
    launch_date,
    memory_gb,
    fp16_tflops,
    tdp_watts,
    estimated_shipments_units,
    estimated_asp_usd,
    estimated_revenue_usd_m,
    description
from {{ source('raw', 'ai_chip_market') }}
where launch_date is not null
