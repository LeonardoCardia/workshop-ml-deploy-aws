import tkinter as tk     # Biblioteca padrão do Python para criar interfaces gráficas
import requests          # Biblioteca para realizar requisições HTTP (chamadas à API)

# URL da API hospedada na sua instância EC2 na AWS
API_URL = "http://3.91.82.112:8000/predict"

def analisar_sentimento():
    comentario = entry_comentario.get() # Obtém o texto digitado pelo usuário no campo de entrada
    if not comentario:
        label_resultado.config(text="Digite um comentário.")
        return # Sai da função sem prosseguir

    try:
        # Envia o comentário para a API (requisição HTTP POST)
        # timeout=5 define um tempo máximo de espera de 5 segundos pela resposta da API.
        resp = requests.post(API_URL, json={"comentario": comentario}, timeout=5)
        
        # Se a API responder com sucesso (código 200)
        if resp.status_code == 200:
            data = resp.json() # Converte a resposta JSON em dicionário
            sentimento = data.get("sentimento", "chave não encontrada: sem resposta") 
            label_resultado.config(text=f"Sentimento: {sentimento}") # Exibe o sentimento na tela
        else: # Caso a API retorne erro (ex: 404 ou 500)
            label_resultado.config(text=f"Erro na API: {resp.status_code}")
    except Exception as e:
        label_resultado.config(text=f"Falha ao conectar: {e}")

def limpar_campos():
    entry_comentario.delete(0, tk.END)  # Apaga todo o texto digitado no campo de entrada
    label_resultado.config(text="")  # Remove o texto exibido na label de resultado
    
################################
# Criação da Interface Gráfica #
################################

# janela principal
root = tk.Tk()                      # Cria a janela principal
root.title("Análise de Sentimento") # Define o título da janela

# Label de instrução acima do campo de texto
tk.Label(root, text="Digite o comentário:").pack(pady=5) # Adiciona 5 pixels de margem superior e inferior.

# Campo de entrada de texto onde o usuário digita o comentário
entry_comentario = tk.Entry(root, width=60)
entry_comentario.pack(pady=5)

# Frame para agrupar os botões lado a lado
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

# Botão que executa a análise de sentimento
btn_analisar = tk.Button(frame_botoes, text="Analisar", command=analisar_sentimento)
btn_analisar.pack(side=tk.LEFT, padx=5)

# Botão que limpa o campo e o resultado
btn_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar_campos)
btn_limpar.pack(side=tk.LEFT, padx=5)

# Label que exibirá o resultado (positivo/negativo)
label_resultado = tk.Label(root, text="", fg="blue")
label_resultado.pack(pady=10)

# Loop principal da interface (mantém a janela aberta)
root.mainloop()
