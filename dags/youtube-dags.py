from datetime import timedelta
from airflow import DAG
from airflow.operators import bash_operator
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

# Define dag variables
project_id = 'zinc-forge-399014'
staging_dataset = 'youtube_dwh_staging'
dwh_dataset = 'youtube_dwh_production'
gs_bucket = 'bigdata-python'

# Define dag_args
default_dag_args = {
        "start_date":  days_ago(1),
        "gcp_conn_id" : "gcp_connection_key",
        "retries": 3,
        "retry_delay": timedelta(minutes=5)
}

# Define dag
dag = DAG('newegg-cloud-data-lake-pipeline',
            schedule_interval = "0 5 * * *",
            default_args=default_dag_args)

start_pipeline = DummyOperator(
    task_id='start_pipeline',
    dag=dag,
)

crawl_data = bash_operator.BashOperator(
    task_id="craw_datas",
    bash_command="python3 /home/quoccong-workspace/airflow_project/scripts/crawl/main.py ",
    dag=dag,
)

extract_data = bash_operator.BashOperator(
    task_id="extract_data",
    bash_command="bash /home/quoccong-workspace/airflow_project/scripts/shell/extract_data.sh ",
    dag=dag,
)

migrate_data = bash_operator.BashOperator(
    task_id="extract_data",
    bash_command="bash /home/quoccong-workspace/airflow_project/scripts/shell/migrate_data.sh ",
    dag=dag,
)

start_pipeline >> crawl_data >> extract_data >> migrate_data

