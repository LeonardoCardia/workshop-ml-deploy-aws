# 🚀 Deploy de Machine Learning na AWS

**Do Notebook a uma API na Amazon EC2**  
Workshop prático · **60 minutos** · **AWS Academy Learner Lab**

Neste workshop, vamos disponibilizar na nuvem um modelo de **análise de sentimentos** treinado com **NLTK e Naive Bayes**. A aplicação usa **FastAPI** e será executada em uma instância **Amazon EC2**, sem precisar instalar Docker.

> **Objetivo:** ao final da atividade, cada participante terá executado uma API de Machine Learning na AWS e realizado uma predição pelo navegador.
>
> **Nota:** esta é uma implantação **didática**. Para produção real, ainda seriam necessários HTTPS, controle de acesso, execução como serviço e monitoramento.

## 🧭 Arquitetura da solução

```text
Notebook de treinamento
         │
         ▼
Modelo treinado (.pkl)
         │
         ▼
FastAPI (api/api.py)
         │
         ▼
Amazon EC2 — AWS Learner Lab
         │
         ▼
Navegador / Swagger UI (/docs)
```

## 📁 Organização do projeto

```text
workshop-ml-deploy-aws/
├── api/
│   ├── __init__.py
│   └── api.py                      # API de inferência com FastAPI
├── app_client/
│   └── ui_interface.py             # Interface opcional em Tkinter
├── data/
│   └── comentario_label.csv        # Base de comentários
├── docs/                           # Materiais de apoio
├── model/
│   └── model_sentiment.pkl         # Modelo treinado
└── notebooks/
    └── Treinamento_Analise_Sentimento.ipynb
```

> O notebook e o dataset mostram como o modelo foi construído. **Durante o workshop, utilizaremos o modelo já treinado** para concentrar o tempo no deploy da AWS.

## ✅ Antes de começar

- Ter acesso à turma no **AWS Academy Learner Lab**.
- Conseguir iniciar o laboratório e abrir o **AWS Management Console**.
- Ter acesso ao repositório público do workshop no GitHub.
- Usar a região e o tipo de instância indicados pelo instrutor, respeitando as restrições do Learner Lab.

**Não é necessário instalar Docker, Python ou VS Code no computador pessoal.** Os comandos serão executados no terminal da EC2.

## ☁️ Passo 1 — Criar sua instância EC2

1. No Learner Lab, clique em **Start Lab** e aguarde o laboratório ficar disponível.
2. Abra o **AWS Console**.
3. Pesquise por **EC2** e selecione **Launch instance**.
4. Escolha um nome, por exemplo, `ml-workshop-aluno`.
5. Selecione uma imagem **Ubuntu Server LTS** e o tipo de instância informado pelo professor.
6. Configure o acesso para **EC2 Instance Connect** conforme as orientações do laboratório.
7. Inicie a instância e aguarde o status **Running**.

> **Segurança:** não distribua chaves privadas `.pem`. Nas regras de entrada (*Security Group*), restrinja o acesso sempre que possível. A porta **8000/TCP** será utilizada apenas para a demonstração da API; limite sua origem ao **seu IP público (/32)**, em vez de deixá-la aberta para toda a internet. A regra para SSH/Instance Connect depende da configuração do laboratório.

## 💻 Passo 2 — Conectar ao servidor

No console EC2, selecione sua instância e clique em **Connect → EC2 Instance Connect** (quando habilitado no laboratório).

No terminal Ubuntu, prepare os programas necessários:

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip
```

## 📥 Passo 3 — Obter o projeto no GitHub

Substitua `SEU_USUARIO` pelo usuário ou organização onde o professor publicou o repositório:

```bash
git clone https://github.com/SEU_USUARIO/workshop-ml-deploy-aws.git
cd workshop-ml-deploy-aws
```

## 🐍 Passo 4 — Preparar o ambiente Python

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as bibliotecas utilizadas na API:

```bash
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" joblib nltk
```

Baixe os recursos necessários ao processamento de textos em português:

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

> **Atenção ao caminho do modelo:** como o arquivo `api.py` fica em `api/` e o modelo fica em `model/`, o carregamento no `api/api.py` deve utilizar um caminho baseado na localização do arquivo:
>
> ```python
> from pathlib import Path
> MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "naive_bayes_classificador.pkl"
> modelo = joblib.load(MODEL_PATH)
> ```
>
> Não utilize apenas `"naive_bayes_classificador.pkl"`, pois a API pode não encontrar o modelo.

## ▶️ Passo 5 — Iniciar a API na EC2

Na raiz do projeto, com o ambiente virtual ativado:

```bash
python -m uvicorn api.api:app --host 0.0.0.0 --port 8000
```

Quando o terminal mostrar que o servidor iniciou, **mantenha essa sessão aberta** durante os testes.

O comando usa:

- `api.api`: pasta `api/` e arquivo `api.py`;
- `app`: objeto `FastAPI` definido nesse arquivo;
- `0.0.0.0`: permite receber conexões pela rede;
- `8000`: porta de acesso à aplicação.

## 🧪 Passo 6 — Testar a API

1. Copie o **Public IPv4 address** da sua instância EC2.
2. Verifique se o *Security Group* permite acesso à porta **8000** a partir do seu IP.
3. No navegador, abra:

```text
http://SEU_IP_PUBLICO:8000/docs
```

4. No Swagger UI, localize **POST /predict**.
5. Clique em **Try it out**, informe o comentário e selecione **Execute**.

**Exemplo de requisição:**

```json
{
  "comentario": "O atendimento foi excelente!"
}
```

**Formato da resposta:**

```json
{
  "sentimento": "positivo",
  "confianca": 0.91
}
```

*A resposta acima é apenas ilustrativa: o rótulo e o número retornados dependem do modelo treinado. A pontuação não deve ser interpretada automaticamente como probabilidade calibrada.*

**Desafio rápido:** teste um comentário positivo, um negativo e um ambíguo. O modelo classifica todos corretamente?

### Teste adicional pelo terminal (opcional)

Na EC2, abra outro terminal e execute:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"comentario":"O produto chegou quebrado"}'
```

O projeto também possui a rota **POST `/predict_batch`** para classificar uma lista de comentários, mas ela fica como exploração adicional.

## 🛠️ Problemas comuns

| Problema | O que verificar |
|---|---|
| `ModuleNotFoundError` | Ative `.venv` e instale as bibliotecas. |
| `FileNotFoundError` para o `.pkl` | Confira o caminho do modelo em `api/api.py`. |
| Erro com `stopwords`, `punkt` ou `punkt_tab` | Execute o comando de download do NLTK. |
| O `/docs` não abre | Confirme IP público, porta 8000 no Security Group e Uvicorn em execução. |
| `Connection refused` | Verifique se o processo Uvicorn iniciou corretamente. |
| `git clone` falhou | Verifique o endereço, a visibilidade pública do repositório e o acesso à internet da EC2. |

## 🧹 Passo 7 — Encerrar e evitar custos

Ao terminar a atividade:

1. No terminal, pressione **Ctrl+C** para parar a API.
2. No AWS Console, acesse **EC2 → Instances**.
3. Selecione a instância criada no workshop e escolha **Instance state → Terminate instance**.
4. Confirme a exclusão e confira se não ficaram recursos adicionais, como volumes EBS ou endereços IP elásticos.
5. Encerre a sessão do Learner Lab conforme as orientações do professor.

> **Importante:** clicar apenas em **End Lab** não substitui a conferência e a remoção dos recursos utilizados. Serviços AWS podem consumir o orçamento do laboratório enquanto estiverem provisionados.

## 📚 Tecnologias utilizadas

**AWS Academy Learner Lab** · **Amazon EC2** · **Ubuntu** · **Python** · **NLTK / Naive Bayes** · **Joblib** · **FastAPI** · **Uvicorn** · **GitHub**

---

**Resultado esperado:** uma API de análise de sentimentos funcionando na Amazon EC2, acessível pelo Swagger UI durante a atividade.
