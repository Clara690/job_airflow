FROM ubuntu:22.04

# system-level setup 
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# install python
RUN uv python install 3.11

WORKDIR /job_airflow


COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# now copy the actual project code
COPY ./pyproject.toml /job_airflow
COPY ./uv.lock /job_airflow
COPY ./dataflow /job_airflow/dataflow
# no CMD/ENTRYPOINT here on purpose — docker-compose-airflow.yml supplies
# a different command per service (webserver, scheduler, worker, etc.)
