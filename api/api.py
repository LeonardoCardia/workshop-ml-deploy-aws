"""API de análise de sentimentos - Workshop AWS Academy Learner Lab.

O modelo já está treinado: nesta aula nós apenas publicamos a inferência.
"""
from pathlib import Path
import string

import joblib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pydantic import BaseModel
from pathlib import Path


# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
# Localização do modelo treinado
MODEL_PATH = BASE_DIR / "model" / "model_sentiment.pkl"


# 1. Cria a API e carrega o modelo UMA única vez ao iniciar o servidor.
app = FastAPI(title="Análise de Sentimentos - Workshop AWS")

# Carregar o modelo
modelo = joblib.load(MODEL_PATH)


stop_words = set(stopwords.words("portuguese"))


# 2. Formato do JSON esperado: {"comentario": "Excelente qualidade, superou minhas expectativas."}.
class Comentario(BaseModel):
    comentario: str


# 3. Repete o pré-processamento utilizado no treinamento original.
def extrair_features(texto: str) -> dict:
    tokens = word_tokenize(texto.lower())
    return {palavra: True for palavra in tokens
            if palavra not in stop_words and palavra not in string.punctuation}


# 4. Rota de verificação: a API está funcionando?
@app.get("/health")
def health():
    return {"status": "ok"}


# 5. Rota principal: recebe o texto e retorna o sentimento previsto.
@app.post("/predict")
def predict(dados: Comentario):
    if not dados.comentario.strip():
        return {"erro": "Digite um comentário não vazio."}
    features = extrair_features(dados.comentario)
    sentimento = modelo.classify(features)
    return {"sentimento": sentimento}

# Disponibilizar a interface HTML na página inicial
@app.get("/")
def pagina_inicial():
    html_path = (
        Path(__file__).resolve().parent.parent
        / "app_client"
        / "index.html"
    )

    return FileResponse(html_path)