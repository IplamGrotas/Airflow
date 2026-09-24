import pandas as pd

def extract_xlsx(**kwargs):
    id_planilha = "1JgB6lNEdO4riMbu25DrFJkgUWoR6EEa2"
    url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=xlsx"

    df = pd.read_excel(url, sheet_name = "andamento_1_etapa_")

    return df