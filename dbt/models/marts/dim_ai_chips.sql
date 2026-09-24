select
    {{ dbt_utils.generate_surrogate_key(['vendor', 'chip_name']) }} as chip_key,
    chip_name,
    vendor,
    launch_date,
    memory_gb,
    fp16_tflops,
    tdp_watts,
    description
from {{ ref('stg_ai_chip_market') }}
-- The source has one row per chip per year; keep only the earliest year's row
-- so this dimension is one row per chip.
qualify row_number() over (partition by vendor, chip_name order by year) = 1
