# 🌤️ AtmosFlow: Enterprise Real-time Weather Data Platform

![Docker](https://img.shields.io/badge/Docker-24//blue?style=flat-square&logo=docker)
![Kafka](https://img.shields.io/badge/Apache_Kafka-yellow?style=flat-square&logo=apache-kafka)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql)
![dbt](https://img.shields.io/badge/dbt-FF642E?style=flat-square&logo=dbt)
![Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat-//square&logo=apache-airflow)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana)

AtmosFlow is a professional-grade real-time data pipeline designed to ingest, transform, and visualize weather data from multiple cities. This project implements a **Medallion Architecture** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) to ensure data quality, reliability, and high-performance analytics.

## 🏗️ System Architecture

The platform follows a decoupled, event-driven architecture:

```Mermaid
flowchart LR
    subgraph Ingestion Layer
        A[OpenWeatherMap API]
        B[Python Producer]
    end

    subgraph Streaming Layer
        C[Apache Kafka]
    end

    subgraph Processing Layer
        D[Python Consumer]
    end

    subgraph Storage Layer
        E[PostgreSQL Bronze]
    end

    subgraph Transformation Layer
        F[dbt Silver]
        G[dbt Gold]
    end

    subgraph Visualization Layer
        H[Grafana Dashboard]
    end

    A --> B --> C --> D --> E --> F --> G --> H
```

### 🛠 Tech Stack & Justification
- **Apache Kafka:** Used as a distributed message broker to decouple ingestion and storage, ensuring the system is fault-tolerant and can handle high-velocity streaming data.
- **PostgreSQL:** Serves as the primary data warehouse, providing strong ACID compliance and robust SQL support.
- **dbt (data build tool):** Implements the transformation layer, converting raw JSON-like data into analytics-ready tables through modular SQL.
- **Apache Airflow:** Orchestrates the dbt transformation pipeline, automating the update of the Gold layer on a scheduled basis.
- **Grafana:** Provides a real-time observability layer for monitoring weather metrics and system health.
- **Docker & Compose:** Ensures complete environment isolation and one-click deployment for the entire ecosystem.

---

## 💎 Data Engineering Approach: Medallion Architecture

To optimize query performance for the dashboard, I implemented a three-layer data strategy:

1. **Bronze Layer (`raw_weather`):** Ingests raw data directly from Kafka. It preserves the original state of the data for auditing and reprocessing.
2. **Silver Layer (`silver_weather`):** A cleansed view that handles data type casting, rounding, and removes NULL values, providing a "single source of truth."
3. **Gold Layer (`gold_daily_summary`):** A materialized table containing pre-aggregated metrics (Avg/Max/Min temperature) per city per day. This ensures the Grafana dashboard loads instantly regardless of data volume.

---

## 🧠 Key Engineering Challenges & Solutions

As a Data Engineer, I focused on solving real-world infrastructure bottlenecks:

### 1. The "Advertised Listener" Trap in Docker
- **Challenge:** Producer failed to connect to Kafka due to `localhost` resolution errors inside the Docker network.
- **Solution:** Implemented a **Dual-Listener configuration**. Defined `PLAINTEXT` for external host access and `PLAINTEXT_INTERNAL` for container-to-container communication, resolving the metadata mismatch.

### 2. Database Boot-up Race Condition
- **Challenge:** The Consumer crashed on startup because it attempted to connect to PostgreSQL before the database was fully initialized.
- **Solution:** Developed a **Robust Retry Logic** with exponential backoff in the `WeatherDBClient`, ensuring the application gracefully waits for the DB to become available.

### 3. Dependency Hell & Environment Isolation
- **Challenge:** Severe version conflicts between `dbt-core` and `mashumaro` libraries on Windows.
- **Solution:** **Containerized the dbt environment**. By running dbt inside a dedicated Docker container, I eliminated host OS dependency issues and ensured 100% reproducibility.

### 4. Pipeline Orchestration
- **Challenge:** Manual execution of dbt transformations is not scalable for production.
- **Solution:** Integrated **Apache Airflow** to automate the dbt run process, transforming the pipeline from a manual script to a scheduled, production-ready workflow.

---

## 🏃 Quick Start

### Prerequisites
- Docker & Docker Compose installed.
- An API Key from [OpenWeatherMap](https://openweathermap.org/api).

### Installation & Deployment
1. **Clone the repository:**
   ```bash
   git clone https://github.com/kina2711/atmosflow.git
   cd atmosflow
   ```
2. **Configure Environment:**

   Create a .env file in the root directory:
   ```.env
   POSTGRES_USER=atmos_admin
   POSTGRES_PASSWORD=atmos_123
   POSTGRES_DB=atmos//db
   KAFKA_BROKER_INTERNAL=kafka:29092
   KAFKA_TOPIC=weather_data
   WEATHER_API_KEY=your_api_key_here
   ```
3. **Launch the Platform:**
   ```Bash
   docker-compose up --build -d
   ```
4. **Trigger First Transformation:**
   ```Bash
   docker run --rm --network atmosflow_default -v ${PWD}/dbt_project:/usr/app -v ${PWD}/.dbt:/root/.dbt ghcr.io/dbt-labs/dbt-postgres:1.7.0 run
   ```
### Monitoring
   - Kafka UI: http://localhost:8080
   - Airflow UI: http://localhost:8081 (User: admin / Pass: admin)
   - Grafana Dashboard: http://localhost:3000 (User: admin / Pass: admin_pass_123)