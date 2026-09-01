FROM ubuntu:22.04

# update dependencies and install curl and ca-certificates
RUN apt-get update && \
    apt-get install -y curl ca-certificates

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# install python 
RUN uv python install 3.11

# make working directory
RUN mkdir /job_airflow

# copy currecnt directory
COPY ./dataflow /job_airflow/dataflow
COPY ./genenv.py /job_airflow
COPY ./pyproject.toml /job_airflow
COPY ./uv.lock /job_airflow
COPY ./README.md /job_airflow
COPY ./local.ini /job_airflow
COPY ./airflow.cfg /job_airflow/airflow.cfg
COPY ./get_sql_conn.sh /job_airflow/get_sql_conn.sh
COPY ./airflow-gce.cfg /job_airflow/airflow-gce.cfg
COPY ./entrypoint.sh /job_airflow/entrypoint.sh
RUN chmod +x /job_airflow/get_sql_conn.sh /job_airflow/entrypoint.sh

# set working directory
WORKDIR /job_airflow

# install dependencies
RUN uv sync --frozen

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN echo "UTC" > /etc/timezone

# create .env
RUN ENV=DOCKER uv run python genenv.py

# airflow
ARG AIRFLOW_USER_HOME=/job_airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

ENTRYPOINT ["/job_airflow/entrypoint.sh"]

# default -> bash
CMD ["/bin/bash"]