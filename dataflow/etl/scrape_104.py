import json
from airflow.decorators import task
from airflow.providers.docker.operators.docker import (
    DockerOperator,
)
from airflow.models import Variable

# define the number of pages to scrape for each term
PAGES_PER_TERM = 10


@task
def build_scrape_commands() -> list[list[str]]:
    # Variable.get() runs here, at task execution time, not at DAG-parse time
    search_terms = json.loads(
        Variable.get('job_search_terms', default_var='["資料工程師"]')
    )
    return [
        [
            'uv', 'run', 'python', '-m', 'scraper.cli_104',
            '--search-term', term,
            '--page', str(page),
        ]
        for term in search_terms
        for page in range(1, PAGES_PER_TERM + 1)
    ]


def create_104_scraper() -> DockerOperator:
    return DockerOperator.partial(
        task_id = 'producer_scraper_104',
        image ='clara690/scraper:0.1.1',
        network_mode = 'my_swarm_network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove = 'success',
        max_active_tis_per_dag = 2,
    ).expand(
        command=build_scrape_commands()
    )