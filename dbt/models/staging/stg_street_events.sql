with source as (
    select * from {{source('staging', 'external_street_events')}}
),

renamed as (
    select
        dt_registo as event_date,	
        area as event_category, 
        tipo as event_type,
        Freguesia as municipal_parish,
        Subseccao as municipal_subsection,
        Longitude_Subseccao as lon_subsection,
        Latitude_Subseccao as lat_subsection
    
    from source
)

select * from renamed


