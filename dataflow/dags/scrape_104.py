from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from dataflow.constant import DEFAULT_ARGS, MAX_ACTIVE_RUNS

with DAG(
    dag_id='scrape_104',
    default_args=DEFAULT_ARGS,
    schedule=None, # manual trigger for now
    catchup=False,
    max_active_runs=MAX_ACTIVE_RUNS,
    tags=['scraper'],
) as dag:
    DockerOperator(
        task_id='scrape_104_p1',
        image='clara690/scraper:0.1.0',
        command='uv run python -m scraper.cli_104 --search-term 軟體工程師 --page 1',
        network_mode='my_swarm_network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )