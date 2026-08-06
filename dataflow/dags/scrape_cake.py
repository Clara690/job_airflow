from airflow import DAG
from dataflow.constant import DEFAULT_ARGS, MAX_ACTIVE_RUNS
from dataflow.etl.scrape_cake import(
    create_cake_scraper,
)

with DAG(
    dag_id='scrape_cake',
    default_args=DEFAULT_ARGS,
    schedule=None, # manual trigger for now
    catchup=False,
    max_active_runs=MAX_ACTIVE_RUNS,
    tags=['scraper', 'cake'],
) as dag:
    create_cake_scraper()