import duckdb
import pandas as pd
from sqlalchemy import text
from sqlalchemy.types import Date
from airflow.providers.mysql.hooks.mysql import MySqlHook

def mysql_load(**kwargs):
    df = kwargs["ti"].xcom_pull(task_ids = "silver_processing")

    df = duckdb.sql("""
        SELECT
            logradouro,
            cidade,
            quadra,
            lote,
            latitude,
            longitude,
            area,
            reurb_e,
            status_processo,
            status_processo_simples,
            data_cadastro,
            data_deferimento,
            proprietario_mat,
            matricula,
            bairro
        FROM df
    """).df()

    mysql_hook = MySqlHook(
        mysql_conn_id = "comunidadesurbanas_mysql"
    )

    engine = mysql_hook.get_sqlalchemy_engine()

    with engine.connect() as conn:
        conn.execute(
            text("TRUNCATE TABLE minha_casa_legal")
        )
        conn.commit()

    df.to_sql(
        name = "minha_casa_legal",
        con = engine,
        if_exists = "append",
        index = False,
        dtype = {
            "data_cadastro": Date(),
            "data_deferimento": Date()
        }
    )