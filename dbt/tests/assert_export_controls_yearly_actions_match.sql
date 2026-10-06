with yearly as (
    select
        year,
        sum(actions) as total_actions
    from {{ ref('fct_export_controls_yearly') }}
    group by year
),

actual as (
    select
        year,
        count(*) as total_actions
    from {{ ref('fct_export_controls') }}
    group by year
)

select
    coalesce(yearly.year, actual.year) as year
from yearly
full outer join actual on yearly.year = actual.year
where coalesce(yearly.total_actions, 0) != coalesce(actual.total_actions, 0)
