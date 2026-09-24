from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
import pendulum, os, sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.minha_casa_legal.mysql.bronze import extract_xlsx
from src.minha_casa_legal.mysql.silver import silver_processing
from src.minha_casa_legal.mysql.gold import mysql_load
from src.minha_casa_legal.postgres.mysql_to_postgres import mysql_to_postgres

with DAG(
    dag_id = "minha_casa_legal",
    schedule = "0 21 * * 5",
    max_active_runs = 1,
    default_args = {
        "owner": "airflow",
        "retries": 1,
        "start_date": pendulum.datetime(2026, 9, 20, tz = "America/Sao_Paulo")
    },
    template_searchpath = ["/opt/airflow/src/minha_casa_legal"],
    catchup = False,
    tags = ["REURB", "reurb", "Reurb", "Minha Casa Legal"]
) as dag:

    e_xlsx = PythonOperator(
        task_id = "extract_xlsx",
        python_callable = extract_xlsx
    )

    silver_prcs = PythonOperator(
        task_id = "silver_processing",
        python_callable = silver_processing
    )

    mysql_ld = PythonOperator(
        task_id = "mysql_load",
        python_callable = mysql_load
    )

    ct_postgres = SQLExecuteQueryOperator(
        task_id = "create_table_postgres",
        conn_id = "comunidadesurbanas_postgres",
        sql = "postgres/create_table.sql"
    )

    unq_idx = SQLExecuteQueryOperator(
        task_id = "create_unique_index",
        conn_id = "comunidadesurbanas_postgres",
        sql = "postgres/create_unique_index.sql"
    )

    postgre_ld = PythonOperator(
        task_id = "postgres_load",
        python_callable = mysql_to_postgres
    )

e_xlsx >> silver_prcs >> mysql_ld >> ct_postgres >> unq_idx >> postgre_ld