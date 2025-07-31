from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# Coloque aqui o link direto para seu arquivo XLSX (pode ser Box, Drive, etc.)
EXCEL_URL = "https://app.box.com/index.php?rm=box_download_shared_file&shared_name=8ewbh7o41cur40tpxfco7rk5pzsjfuho&file_id=f_1941672106811"

@app.get("/")
def home():
    return {"msg": "API do Excel no ar!"}

@app.get("/busca")
def busca(termo: str = Query(..., description="Palavra-chave para busca")):
    try:
        # Lê direto do link
        df = pd.read_excel(EXCEL_URL)
        # Busca apenas na coluna de palavras-chave
        resultados = df[df["PALAVRAS_CHAVE_DICIONARIO"].str.contains(termo, case=False, na=False)]
        # Retorna colunas desejadas
        dados = resultados[["TITULO", "ASSUNTO", "TEXTO_CONSOLIDADO"]].to_dict(orient="records")
        return dados
    except Exception as e:
        return {"erro": str(e)}


