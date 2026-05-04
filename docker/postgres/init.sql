-- Tạo Schema cho dữ liệu thô
CREATE TABLE IF NOT EXISTS raw_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature NUMERIC(5, 2),
    humidity INTEGER,
    description TEXT,
    event_time TIMESTAMP WITH TIME ZONE, 
    processed_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tạo Index để tối ưu Query
CREATE INDEX idx_weather_city ON raw_weather(city);
CREATE INDEX idx_weather_event_time ON raw_weather(event_time);