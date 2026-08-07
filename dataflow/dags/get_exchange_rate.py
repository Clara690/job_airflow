from airflow import DAG
from dataflow.constant import DEFAULT_ARGS, MAX_ACTIVE_RUNS
from dataflow.etl.get_exchange_rate import(
    create_exchange_rate_scraper,
)

with DAG(
    dag_id='get_exchange_rate',
    default_args=DEFAULT_ARGS,
    schedule='0 9 * * *', # update daily at 9am
    catchup=False,
    max_active_runs=MAX_ACTIVE_RUNS,
    tags=['scraper', 'exchange_rate'],
) as dag:
    create_exchange_rate_scraper()