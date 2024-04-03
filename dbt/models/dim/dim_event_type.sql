{{
    config(
        materialized='table'
    )
}}


select ROW_NUMBER ()
	OVER (PARTITION BY 1 order by event_type) as id, event_type, max(dim_ec.id) as event_category_id
from {{ ref('stg_street_events') }} as stg
join {{ ref('dim_event_category') }} as dim_ec on dim_ec.event_category = stg.event_category
group by event_type

