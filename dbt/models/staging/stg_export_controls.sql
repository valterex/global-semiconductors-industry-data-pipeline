select
    control_id,
    date as enacted_date,
    year,
    month,
    imposing_country,
    target as target_country,
    policy_name,
    severity_score,
    description,
    cast(is_trump_1_0 as boolean) as is_trump_first_term,
    cast(is_biden as boolean) as is_biden_term,
    cast(is_trump_2_0 as boolean) as is_trump_second_term
from {{ source('raw', 'export_controls') }}
where date is not null
