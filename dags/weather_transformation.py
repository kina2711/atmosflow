from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Định nghĩa DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'atmosflow_dbt_transformation',
    default_args=default_args,
    description='Run dbt transformation for weather data',
    schedule_interval='*/15 * * * *',
    catchup=False
) as dag:

    run_dbt = BashOperator(
        task_id='dbt_run',
        # Gọi trực tiếp vào container dbt
        bash_command='docker exec atmosflow-dbt dbt run --project-dir /usr/app --profiles-dir /root/.dbt'
    )

    run_dbt