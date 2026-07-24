## Deploy airflow 
The following command applies only to `docker-compose-airflow.yml`.
```text
DOCKER_IMAGE_VERSION=0.0.2 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
```