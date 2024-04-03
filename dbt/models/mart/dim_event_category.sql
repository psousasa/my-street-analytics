{{
    config(
        materialized='table'
    )
}}


select ROW_NUMBER ()
	OVER (PARTITION BY 1 order by event_category) as id, event_category
from {{ ref('stg_street_events') }}
group by event_category

