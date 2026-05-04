{{ config(materialized='view') }}

SELECT 
    id,
    city,
    ROUND(temperature, 2) as temp,
    humidity,
    description,
    event_time::DATE as date,
    event_time::TIME as time,
    event_time
FROM {{ source('raw', 'raw_weather') }}
WHERE city IS NOT NULL AND temperature IS NOT NULL