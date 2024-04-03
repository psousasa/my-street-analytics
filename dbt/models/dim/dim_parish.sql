{{
    config(
        materialized='table'
    )
}}


select ROW_NUMBER ()
	OVER (PARTITION BY 1 order by municipal_parish) as id, municipal_parish
from {{ ref('stg_street_events') }}
group by municipal_parish

