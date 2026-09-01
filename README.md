## Deploy airflow 
The following command applies only to `docker-compose-airflow.yml`.
```text
DOCKER_IMAGE_VERSION=0.0.7 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow

DOCKER_IMAGE_VERSION=0.0.8.gce docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
```