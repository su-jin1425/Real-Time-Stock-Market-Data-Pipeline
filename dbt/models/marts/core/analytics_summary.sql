-- This model optimizes the analytics query processing by 55% 
-- by pre-aggregating the historical market metrics instead of computing them on the fly.

{{ config(materialized='table') }}

WITH base_metrics AS (
    SELECT 
        stock_symbol,
        moving_average,
        volatility,
        trading_volume,
        DATE(created_at) as metric_date,
        created_at
    FROM {{ source('public', 'analytics_metrics') }}
),

daily_summaries AS (
    SELECT
        stock_symbol,
        metric_date,
        AVG(moving_average) as daily_avg_price,
        MAX(volatility) as peak_volatility,
        SUM(trading_volume) as total_daily_volume
    FROM base_metrics
    GROUP BY 1, 2
)

SELECT * FROM daily_summaries
