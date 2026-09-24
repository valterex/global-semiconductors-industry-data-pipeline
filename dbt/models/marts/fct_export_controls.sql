select
    control_id,
    enacted_date,
    year,
    month,
    imposing_country,
    target_country,
    policy_name,
    severity_score,
    description,
    case
        when is_trump_first_term then 'Trump 1.0'
        when is_biden_term then 'Biden'
        when is_trump_second_term then 'Trump 2.0'
        else 'Other'
    end as administration
from {{ ref('stg_export_controls') }}
