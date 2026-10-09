"""API de análise de sentimentos - Workshop AWS Academy Learner Lab.

O modelo já está treinado: nesta aula nós apenas publicamos a inferência.
"""
from pathlib import Path
import string

import joblib
from fastapi import FastAPI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pydantic import BaseModel

# 1. Cria a API e carrega o modelo UMA única vez ao iniciar o servidor.
app = FastAPI(title="Análise de Sentimentos - Workshop AWS")
modelo = joblib.load(Path(__file__).with_name("model_sentiment.pkl"))
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