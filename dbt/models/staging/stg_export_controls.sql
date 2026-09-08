select
    control_id,
    date,
    year,
    month,
    imposing_country,
    target,
    policy_name,
    severity_score,
    description,
    is_us_action,
    is_china_action,
    is_netherlands_action,
    is_trump_1_0,
    is_biden,
    is_trump_2_0
from {{ source('raw', 'export_controls') }}
where date is not null
