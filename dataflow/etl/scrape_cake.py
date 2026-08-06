import json 
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.docker.operators.docker import (
    DockerOperator,
)

# define the number of pages to scrape for each term
PAGES_PER_TERM = 5

@task 
def build_scrape_commands() -> list[list[str]]:
    try:
        search_terms = json.loads(
            Variable.get('job_search_terms_cake', default_var='["data engineer"]')
        )
    except json.JSONDecodeError as e:
        raise ValueError(
        f"job_search_terms_cake Airflow Variable isn't valid JSON — "
        f"check Admin > Variables in the UI. Must use double quotes, e.g. "
        f'["Backend Engineer", "Data Engineer"]. Original error: {e}'
    ) from e

    return [
        [
            'uv', 'run', 'python', '-m', 'scraper.cli_cake',
            '--search-term', term,
            '--page', str(page),
        ]
        for term in search_terms
        for page in range(1, PAGES_PER_TERM + 1)
    ]

def create_cake_scraper() -> DockerOperator:
    return DockerOperator.partial(
        task_id = 'producer_scraper_cake',
        image ='clara690/scraper:0.1.1',
        network_mode = 'my_swarm_network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove = 'success',
        max_active_tis_per_dag = 2,
    ).expand(
        command=build_scrape_commands()
    )