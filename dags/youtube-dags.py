from datetime import timedelta
from airflow import DAG
from airflow.operators import bash_operator
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Define dag variables
project_id = 'manifest-setup-397505'
staging_dataset = 'newegg_dwh_staging'
dwh_dataset = 'newegg_dwh_production'
gs_bucket = 'de-airflow-bucket'

# Define dag_args
default_dag_args = {
        "start_date":  days_ago(1)
        ,"gcp_conn_id" : "gcp_connection_key"
        , "retries": 3
        , "retry_delay": timedelta(minutes=5)
        , "email": "quoccong-workspace@gmail.com"
        , "email_on_failure": True
        , "email_on_retry": True
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

load_data_to_gcs = bash_operator.BashOperator(
    task_id="extract_data",
    bash_command="python3 /home/quoccong-workspace/airflow_project/scripts/shell/extract_data.sh ",
    dag=dag,
)
# Load data from GCS to BQ
load_data_to_staging_warehouse = GCSToBigQueryOperator(
   task_id = 'load_data_to_staging_warehouse',
   bucket = gs_bucket,
   source_objects = ["newedge-graphic-cards.csv"],
   destination_project_dataset_table = f'{project_id}:{staging_dataset}.newegg_data',
   autodetect = True,
   write_disposition='WRITE_TRUNCATE',
   source_format = 'CSV',
   encoding = "UTF-8",
   field_delimiter=';',
   skip_leading_rows = 1,
   dag=dag,
)

# Check loaded data not null
check_datas = BigQueryExecuteQueryOperator(
    task_id = 'check_datas',
    use_legacy_sql=False,
    sql = f'SELECT count(*) FROM `{project_id}.{staging_dataset}.newegg_data`',
    dag=dag,
)


loaded_data_to_staging = DummyOperator(
    task_id = 'loaded_data_to_staging',
        dag=dag,
)

# Transform, load, and check fact data
create_newegg_datas_on_production = BigQueryExecuteQueryOperator(
    task_id = 'create_newegg_data',
    use_legacy_sql = False,
    params = {
        'project_id': project_id,
        'staging_dataset': staging_dataset,
        'dwh_dataset': dwh_dataset
    },
    sql = './sql/newegg_dashboard_query.sql',
    dag=dag,
)
start_pipeline >> extract_data >> load_data_to_gcs >> load_data_to_staging_warehouse >> check_datas >> loaded_data_to_staging >> create_newegg_datas_on_production

