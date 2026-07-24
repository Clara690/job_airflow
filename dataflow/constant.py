import datetime  

# default param, will be used in DAG and Task 
DEFAULT_ARGS = {
    # DAG/Task manager, will show pu on Airflow UI 
    "owner": "job-hunter",
    # retry maximum once if fails
    "retries": 1,
    # retry time interval 1 
    "retry_delay": datetime.timedelta(minutes=1),
    # the time when starts DAG 
    "start_date": datetime.datetime(2026, 7, 23),
    # 單一 task 最長可執行 60 分鐘，超時則視為失敗
    "execution_timeout": datetime.timedelta(minutes=60),
    # manimum 10 task for DAG
    "concurrency": 10,
}

# 限制此 DAG 同時最多只能執行一個 run（防止排程或手動重疊執行）
MAX_ACTIVE_RUNS = 1
