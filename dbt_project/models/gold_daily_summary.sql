{{ config(materialized='table') }}

SELECT 
    city,
    date_trunc('day', event_time) as day,
    ROUND(AVG(temp), 2) as avg_temp,
    MAX(temp) as max_temp,
    MIN(temp) as min_temp,
    COUNT(*) as data_points
FROM {{ ref('silver_weather') }}
GROUP BY city, date_trunc('day', event_time)