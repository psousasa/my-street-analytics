{{
    config(
        materialized='table'
    )
}}


select  stg.municipal_subsection_code as id,  -- same as municipal_subsection_code
        max(dim_p.id) as municipal_parish_id,
        max(stg.lon_subsection) as longitude,
        max(stg.lat_subsection) as latitude
from {{ ref('stg_street_events') }} as stg
join {{ ref('dim_parish') }} as dim_p on dim_p.municipal_parish = stg.municipal_parish
group by municipal_subsection_code

