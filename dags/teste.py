from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pendulum
import logging

def teste():
    print("Airflow funcionando corretamente!")
    logging.info("Airflow funcionando corretamente!")

with DAG(
    dag_id = "teste",
    schedule = None,
    start_date = pendulum.datetime(2026, 9, 1, tz="America/Sao_Paulo"),
    catchup = False,
) as dag:

    teste_task = PythonOperator(
        task_id="teste",
        python_callable=teste,
    )