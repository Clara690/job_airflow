from airflow import DAG
from dataflow.constant import DEFAULT_ARGS, MAX_ACTIVE_RUNS
from dataflow.etl.scrape_104 import(
    create_104_scraper,
)

with DAG(
    dag_id='scrape_104',
    default_args=DEFAULT_ARGS,
    schedule='0 9 * * *', # update daily at 9am
    catchup=False,
    max_active_runs=MAX_ACTIVE_RUNS,
    tags=['scraper', '104'],
) as dag:
    create_104_scraper()