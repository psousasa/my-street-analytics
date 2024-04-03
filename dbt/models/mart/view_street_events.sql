{{
    config(
        materialized='view'
    )
}}


select  fact_se.event_date, 
        dim_ec.event_category,
        dim_et.event_type,
        dim_p.municipal_parish,
        dim_ps.longitude, 
        dim_ps.latitude

from {{ ref('fact_street_events') }} as fact_se

join {{ ref('dim_parish_subsection') }} as dim_ps on fact_se.municipal_subsection_code = dim_ps.id
join {{ ref('dim_parish') }} as dim_p on dim_ps.municipal_parish_id = dim_p.id

join {{ ref('dim_event_type') }} as dim_et on fact_se.event_type_id = dim_et.id
join {{ ref('dim_event_category') }} as dim_ec on dim_et.event_category_id = dim_ec.id
