from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Link do arquivo Excel
XLSX_URL = "https://app.box.com/index.php?rm=box_download_shared_file&shared_name=g75ukfevcoym61rquj0k3n3bwdcpn9zd&file_id=f_1940536962947"

@app.route("/busca", methods=["GET"])
def busca():
    termo = request.args.get("termo", "")
    if not termo:
        return jsonify({"erro": "Parâmetro 'termo' não informado."}), 400
    try:
        df = pd.read_excel(XLSX_URL)
        # Busca APENAS na coluna PALAVRAS_CHAVE_DICIONARIO (insensível a maiúsculas/minúsculas)
        mask = df["PALAVRAS_CHAVE_DICIONARIO"].astype(str).str.lower().str.contains(termo.lower())
        # Retorna apenas as colunas principais
        resultados = df.loc[mask, ["TITULO", "ASSUNTO", "PALAVRAS_CHAVE_DICIONARIO", "TEXTO_CONSOLIDADO"]]
        return jsonify(resultados.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/")
def home():
    return "API de busca no arquivo Excel funcionando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

