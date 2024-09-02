from airflow.plugins_manager import AirflowPlugin
from airflow.operators.python import PythonOperator
from airflow.utils.decorators import apply_defaults
from datetime import date
import logging

class PrintExecutionDateOperator(PythonOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(PrintExecutionDateOperator, self).__init__(python_callable=self.print_execution_date, *args, **kwargs)

    def print_execution_date(self, **kwargs):
        logging.info(f"The DAG was executed on: {date.today()}")

class PrintExecutionDatePlugin(AirflowPlugin):
    name = "print_execution_date_plugin"
    operators = [PrintExecutionDateOperator]
