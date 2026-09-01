#!/bin/sh
set -e

# Airflow strips *_cmd config options (e.g. sql_alchemy_conn_cmd) out of the
# config snapshot it hands to raw task subprocesses (tmp_configuration_copy
# is called with include_cmds=False for non-impersonated tasks), so a task
# run silently falls back to the default SQLite backend instead of running
# get_sql_conn.sh. Resolve the secret into a real env var instead: env vars
# are inherited by forked subprocesses and aren't subject to that stripping.
if [ -f /run/secrets/mysql_root_password ]; then
  export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="mysql+pymysql://root:$(cat /run/secrets/mysql_root_password)@mysql/airflow"
fi

exec "$@"
