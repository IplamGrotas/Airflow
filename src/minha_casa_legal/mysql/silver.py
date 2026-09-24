import pandas as pd


def silver_processing(**kwargs):
    df = kwargs["ti"].xcom_pull(task_ids = "extract_xlsx")

    df = df.rename(columns={
        "lat": "latitude",
        "long": "longitude",
        "Reurb-E": "reurb_e",
        "Status Processo_Simples": "status_processo_simples",
        "Status Processo": "status_processo",
        "Data de Cadastro": "data_cadastro",
        "Data de Deferimento": "data_deferimento",
        "Quadra/Lote": "quadra_lote",
        "Proprietário_Mat": "proprietario_mat",
        "Matrícula": "matricula",
        "Bairro": "bairro"
    })

    df["reurb_e"] = df["reurb_e"].map({
        "Sim": True,
        "Não": False
    }).astype("boolean")

    df["data_cadastro"] = pd.to_datetime(
        df["data_cadastro"],
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    df["data_deferimento"] = pd.to_datetime(
        df["data_deferimento"],
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.date

    df["proprietario_mat"] = (
        df["proprietario_mat"]
        .str.upper()
        .str.strip()
        .replace("", None)
    )

    df["bairro"] = (
        df["bairro"]
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    df = df.drop_duplicates(
        subset = ["bairro", "quadra", "lote"],
        keep = "first"
    )

    return df