-- Normally, this would be an insert/update table, with stg only containing the latest ETL data
{{
     config(
    materialized = "table",
    cluster_by=['event_date'],
    partition_by = {
      "field": "event_type_id",
      "data_type": "integer"
    }  )
}}

select  ROW_NUMBER() OVER (Partition by 1 order by stg.event_date) as id, 
        stg.event_date, 
        dim_et.id as event_type_id, 
        stg.municipal_subsection_code
from {{ ref('stg_street_events')}} as stg
join {{ ref('dim_event_type')}}  as dim_et on stg.event_type = dim_et.event_type
