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
COPY ./get_sql_conn.sh /job_airflow/get_sql_conn.sh
COPY ./entrypoint.sh /job_airflow/entrypoint.sh
RUN chmod +x /job_airflow/get_sql_conn.sh /job_airflow/entrypoint.sh

ARG AIRFLOW_USER_HOME=/job_airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# entrypoint resolves the mysql_root_password secret into
# AIRFLOW__DATABASE__SQL_ALCHEMY_CONN before exec'ing the real command —
# raw task subprocesses don't see sql_alchemy_conn_cmd (Airflow strips
# *_cmd options from the config snapshot it hands them), so the DB
# connection must arrive as a real env var instead.
ENTRYPOINT ["/job_airflow/entrypoint.sh"]
# docker-compose-airflow.yml supplies a different command per service
# (webserver, scheduler, worker, etc.)
