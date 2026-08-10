#!/bin/sh
printf '%s' "mysql+pymysql://root:$(cat /run/secrets/mysql_root_password)@mysql/airflow"