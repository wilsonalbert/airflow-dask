from __future__ import print_function
import os
from pprint import pprint
from pathlib import Path
from builtins import range
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.models import DAG

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 11, 10),
    'depends_on_past': False,
    'max_active_runs': 1,
    'concurrency': 4,
    'dagrun_timeout ': timedelta(seconds=30)
}

dag = DAG(
    dag_id=os.path.basename(__file__).replace(".pyc", "").replace(".py", ""),
    default_args=args,
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=True
)


def my_sleeping_function(random_base):
    print("Simple task")


def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    pprint("WORKER ENVIRONMENT VARIABLES_")
    for key, value in os.environ.items():
        pprint(f'{key}={value}')

    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

for i in range(10):
    '''
    Generating 10 sleeping task, sleeping from 0 to 9 seconds
    respectively
    '''
    task = PythonOperator(
        task_id='sleep_for_' + str(i),
        python_callable=my_sleeping_function,
        op_kwargs={'random_base': float(i) / 10},
        dag=dag)

    task.set_upstream(run_this)