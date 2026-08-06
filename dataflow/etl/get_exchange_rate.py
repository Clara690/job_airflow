from airflow.decorators import task
from airflow.providers.docker.operators.docker import (
    DockerOperator,
)

def create_exchange_rate_scraper() -> DockerOperator:
    return DockerOperator(
        task_id = 'producer_scraper_exchange_rate',
        image ='clara690/scraper:0.1.1',
        command = "uv run python -m scraper.cli_exchange_rate",
        force_pull = True,
        network_mode = 'my_swarm_network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove = 'success',
        )
