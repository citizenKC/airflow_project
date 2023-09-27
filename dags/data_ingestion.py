import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from ingestion_script import ingest_data

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")

# url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
URL_PREFIX = "https://d37ci6vzurychx.cloudfront.net/trip-data"
URL_TEMPLATE = (
    URL_PREFIX + "/yellow_tripdata_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
OUTPUT_TEMPLATE = (
    AIRFLOW_HOME + "/output_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
TABLE_TEMPLATE = "yellow_taxi_data"

workflow = DAG(
    dag_id="IngestionDag",
    start_date=datetime(2023, 1, 1),
    #the pattern below runs script at 06:00 on the 1st day of each month
    schedule_interval="0 6 1 * *",
    #use max_active_runs if your tasks tend to fail all at once 
    max_active_runs=1
    end_date = datetime(2023, 7, 1)
)
with workflow:
    curl_task = BashOperator(
        task_id="curl",
        bash_command=f"curl -sSl {URL_TEMPLATE} > {OUTPUT_TEMPLATE}"
        # bash_command="echo \" {{ ds }} {{ execution_date.strftime('%Y-%m') }} \"",
    )
    load_task = PythonOperator(
        task_id="load",
        python_callable=ingest_data,
        op_kwargs=dict(parquet_file=OUTPUT_TEMPLATE, table_name=TABLE_TEMPLATE),
    )

curl_task >> load_task
