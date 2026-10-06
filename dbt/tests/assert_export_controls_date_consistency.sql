select
    control_id
from {{ ref('fct_export_controls') }}
where year != extract(year from enacted_date)
   or month != extract(month from enacted_date)
