from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from print_execution_date_plugin import PrintExecutionDateOperator

import os
import logging

CLONE_DIR = ' /opt/airflow/downloads/projeto_imoveis-coleta'
GITHUB_TOKEN = Variable.get('GITHUB_TOKEN')

@dag(schedule=None, start_date=days_ago(1), catchup=False)
def example_dag():
    
    print_execution_date = PrintExecutionDateOperator(
        task_id='print_execution_date'
    )
    
    @task.bash
    def clone_repository():
        repo_url = f'https://{GITHUB_TOKEN}@github.com/Gustavofh/projeto_imoveis-coleta.git'
        clone_command = f'git clone {repo_url} {CLONE_DIR}'
        return clone_command
    
    @task.bash
    def process_data():
        logging.info('Processing...')
        process_command = f'python {CLONE_DIR}/main.py'
        return process_command
    
    @task.bash
    def cleanup():
        logging.info(f'Removing {CLONE_DIR} repo...')
        return f'rm -rf {CLONE_DIR}'
    
    clone_task = clone_repository()
    process_task = process_data()
    cleanup_task = cleanup()

    print_execution_date >> clone_task >> process_task >> cleanup_task

# Instanciando a DAG
dag = example_dag()