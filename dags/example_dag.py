from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import os

# Definindo o diretório onde o repositório será clonado
CLONE_DIR = ' /opt/airflow/downloads/projeto_imoveis-coleta'

GITHUB_TOKEN = Variable.get('GITHUB_TOKEN')

@dag(schedule=None, start_date=days_ago(1), catchup=False)
def example_dag():
    
    @task.bash
    def clone_repository():
        # Comando para clonar o repositório GitHub
        repo_url = f'https://{GITHUB_TOKEN}@github.com/Gustavofh/projeto_imoveis-coleta.git'
        clone_command = f'git clone {repo_url} {CLONE_DIR}'
        return clone_command
    
    @task.bash
    def process_data():
        print('Processando dados...')
        process_command = f'python {CLONE_DIR}/main.py'
        return process_command
    
    @task.bash
    def cleanup():
        # Limpeza após o processamento
        print(f'Removendo diretório {CLONE_DIR}...')
        return f'rm -rf {CLONE_DIR}'
    
    # Definindo a ordem de execução das tarefas
    clone_task = clone_repository()
    process_task = process_data()
    cleanup_task = cleanup()

    clone_task >> process_task >> cleanup_task

# Instanciando a DAG
dag = example_dag()