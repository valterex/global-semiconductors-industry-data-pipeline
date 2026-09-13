{{
    config(materialized="view")
}}

select
    year,
    administration,
    count(*) as actions
from {{ ref('fct_export_controls') }}
group by year, administration
