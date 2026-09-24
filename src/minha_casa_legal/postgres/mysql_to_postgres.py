import pandas as pd
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import text


def mysql_to_postgres(**kwargs):
    mysql_hook = MySqlHook(
        mysql_conn_id="comunidadesurbanas_mysql"
    )

    mysql_engine = mysql_hook.get_sqlalchemy_engine()

    df = pd.read_sql(
        "SELECT * FROM minha_casa_legal",
        mysql_engine
    )

    df["reurb_e"] = df["reurb_e"].astype("boolean")

    postgres_hook = PostgresHook(
        postgres_conn_id="comunidadesurbanas_postgres"
    )

    postgres_engine = postgres_hook.get_sqlalchemy_engine()

    df.to_sql(
        name = "minha_casa_legal_staging",
        con = postgres_engine,
        schema = "public",
        if_exists = "replace",
        index = False
    )

    with postgres_engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO reurb.minha_casa_legal (
                id,
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
            )
            SELECT
                id,
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
            FROM public.minha_casa_legal_staging

            ON CONFLICT (bairro, quadra, lote)
            DO UPDATE SET
                id = EXCLUDED.id,
                logradouro = EXCLUDED.logradouro,
                cidade = EXCLUDED.cidade,
                quadra = EXCLUDED.quadra,
                lote = EXCLUDED.lote,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                area = EXCLUDED.area,
                reurb_e = EXCLUDED.reurb_e,
                status_processo = EXCLUDED.status_processo,
                status_processo_simples = EXCLUDED.status_processo_simples,
                data_cadastro = EXCLUDED.data_cadastro,
                data_deferimento = EXCLUDED.data_deferimento,
                proprietario_mat = EXCLUDED.proprietario_mat,
                matricula = EXCLUDED.matricula
        """))

        conn.execute(text("""
            DROP TABLE public.minha_casa_legal_staging
        """))