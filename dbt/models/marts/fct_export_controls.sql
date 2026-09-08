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
    cast(is_us_action as boolean) as is_us_action,
    cast(is_china_action as boolean) as is_china_action,
    cast(is_netherlands_action as boolean) as is_netherlands_action,
    case
        when is_trump_1_0 = 1 then 'Trump 1.0'
        when is_biden = 1 then 'Biden'
        when is_trump_2_0 = 1 then 'Trump 2.0'
        else 'Other'
    end as administration
from {{ ref('stg_export_controls') }}
