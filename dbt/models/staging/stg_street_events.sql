with
    source as (select * from {{ source("staging", "external_street_events") }}),

    renamed as (
        select
            dt_registo as event_date,
            area as event_category,
            tipo as event_type,
            freguesia as municipal_parish,
            subseccao as municipal_subsection_code,
            longitude_subseccao as lon_subsection,
            latitude_subseccao as lat_subsection

        from source
    )

select *
from renamed
