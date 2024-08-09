import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def processar_arquivo(arquivo):
    caminho_arquivo = f"C:\\Users\\Mateus\\Desktop\\Editar\\{arquivo}.mp4"
    
    if os.path.exists(caminho_arquivo):
        comando = ["auto-editor", caminho_arquivo, "--export", "premiere", "--margin", "0.1sec"]
        try:
            subprocess.run(comando, check=True)
            messagebox.showinfo("Concluído", "Processamento concluído.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
    else:
        messagebox.showerror("Erro", "Arquivo não encontrado. Verifique o nome e tente novamente.")

def on_submit(event=None):
    arquivo = entrada_arquivo.get()
    if arquivo:
        processar_arquivo(arquivo)
    else:
        messagebox.showwarning("Aviso", "Digite o nome do arquivo.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Processador de Vídeos")

tk.Label(root, text="Digite o nome do arquivo (sem extensão):").pack(pady=10)

entrada_arquivo = tk.Entry(root)
entrada_arquivo.pack(pady=5)

botao_processar = tk.Button(root, text="Processar", command=on_submit)
botao_processar.pack(pady=10)

# Associa a tecla Enter ao botão "Processar"
root.bind('<Return>', on_submit)

root.mainloop()
