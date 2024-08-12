import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import ffmpeg

def processar_arquivo(arquivo, margem, saida):
    caminho_arquivo = os.path.join(diretorio_entrada.get(), arquivo)
    
    if os.path.exists(caminho_arquivo):
        # Adiciona o sufixo "_cortado" ao nome do arquivo
        nome, ext = os.path.splitext(arquivo)
        nome_saida = f"{nome}_cortado.xml"
        caminho_saida = os.path.join(saida, nome_saida)
        
        comando = [
            "auto-editor",
            caminho_arquivo,
            "--export", "premiere",
            "--margin", f"{margem}sec",
            "--output", caminho_saida
        ]
        
        try:
            carregando.start()
            subprocess.run(comando, check=True)
            messagebox.showinfo("Concluído", f"Processamento concluído. Arquivo salvo em: {caminho_saida}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo:\n{e.output}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
        finally:
            carregando.stop()
    else:
        messagebox.showerror("Erro", "Arquivo não encontrado. Verifique o nome e tente novamente.")

def on_submit(event=None):
    selecionado = treeview_videos.selection()
    if selecionado:
        item = selecionado[0]
        arquivo = treeview_videos.item(item, 'values')[0]
        margem = entrada_margem.get()
        saida = entrada_saida.get()
        if arquivo and margem and saida:
            processar_arquivo(arquivo, margem, saida)
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
    else:
        messagebox.showwarning("Aviso", "Selecione um vídeo.")

def listar_videos():
    caminho = diretorio_entrada.get()
    if os.path.exists(caminho):
        for item in treeview_videos.get_children():
            treeview_videos.delete(item)
        
        videos = [f for f in os.listdir(caminho) if f.endswith('.mp4')]
        for video in videos:
            imagem_thumbnail = gerar_miniatura(os.path.join(caminho, video))
            treeview_videos.insert('', tk.END, values=(video,), image=imagem_thumbnail)
    else:
        messagebox.showerror("Erro", "Diretório de entrada inválido.")

def gerar_miniatura(arquivo):
    thumbnail_path = "thumbnail.jpg"
    try:
        # Extrai uma miniatura do vídeo usando ffmpeg-python
        ffmpeg.input(arquivo, ss=1).output(thumbnail_path, vframes=1, format='image2', vcodec='mjpeg').run(overwrite_output=True, quiet=True)
        
        # Redimensiona a miniatura
        imagem = Image.open(thumbnail_path)
        imagem.thumbnail((150, 150))
        imagem_tk = ImageTk.PhotoImage(imagem)
        return imagem_tk
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar miniatura: {e}")
        return None

def selecionar_diretorio_entrada():
    caminho = filedialog.askdirectory()
    if caminho:
        diretorio_entrada.set(caminho)
        listar_videos()

def selecionar_arquivo(event=None):
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos MP4", "*.mp4")])
    if arquivo:
        caminho_arquivo = os.path.basename(arquivo)
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho_arquivo)
        mostrar_miniatura(arquivo)

def arrastar_arquivo(event):
    arquivos = event.data.strip('{}').split()
    if arquivos:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, os.path.basename(arquivos[0]))
        mostrar_miniatura(arquivos[0])

def mostrar_miniatura(arquivo):
    thumbnail_path = "thumbnail.jpg"
    try:
        # Extrai uma miniatura do vídeo usando ffmpeg-python
        ffmpeg.input(arquivo, ss=1).output(thumbnail_path, vframes=1, format='image2', vcodec='mjpeg').run(overwrite_output=True, quiet=True)
        
        # Exibe a miniatura na interface gráfica
        imagem = Image.open(thumbnail_path)
        imagem.thumbnail((150, 150))
        imagem_tk = ImageTk.PhotoImage(imagem)
        miniatura_label.config(image=imagem_tk)
        miniatura_label.image = imagem_tk
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar miniatura: {e}")

# Configuração da interface gráfica
root = TkinterDnD.Tk()
root.title("Processador de Vídeos")

# Variável para armazenar o diretório de entrada
diretorio_entrada = tk.StringVar(value="C:\\Users\\Mateus\\Desktop\\Editar")

# Campo para selecionar o diretório de entrada
tk.Label(root, text="Diretório de Entrada:").pack(pady=10)
entrada_diretorio = tk.Entry(root, textvariable=diretorio_entrada, width=50)
entrada_diretorio.pack(pady=5)
botao_diretorio = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio_entrada)
botao_diretorio.pack(pady=10)

# Treeview para exibir vídeos com miniaturas
treeview_videos = ttk.Treeview(root, columns=('Nome'), show='headings')
treeview_videos.heading('Nome', text='Vídeo')
treeview_videos.pack(pady=10, fill=tk.BOTH, expand=True)

# Carregamento de imagens para treeview
treeview_videos.image_list = {}
def carregar_imagens():
    for item in treeview_videos.get_children():
        video = treeview_videos.item(item, 'values')[0]
        imagem_thumbnail = gerar_miniatura(os.path.join(diretorio_entrada.get(), video))
        if imagem_thumbnail:
            treeview_videos.image_list[video] = imagem_thumbnail
            treeview_videos.item(item, image=imagem_thumbnail)

carregar_imagens()

# Label para exibir a miniatura do vídeo
miniatura_label = tk.Label(root)
miniatura_label.pack(pady=10)

# Campo para modificar a margem
tk.Label(root, text="Digite a margem (em segundos):").pack(pady=10)
entrada_margem = tk.Entry(root)
entrada_margem.pack(pady=5)
entrada_margem.insert(0, "0.1")

# Campo para modificar o diretório de saída
tk.Label(root, text="Digite o diretório de saída:").pack(pady=10)
entrada_saida = tk.Entry(root)
entrada_saida.pack(pady=5)
entrada_saida.insert(0, "C:\\Users\\Mateus\\Desktop\\Editar")

# Botão para processar o arquivo
botao_processar = tk.Button(root, text="Processar", command=on_submit)
botao_processar.pack(pady=10)

# ProgressBar de carregamento
carregando = ttk.Progressbar(root, mode="indeterminate")
carregando.pack(pady=10)

# Drag and Drop de arquivos
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', arrastar_arquivo)

# Associa a tecla Enter ao botão "Processar"
root.bind('<Return>', on_submit)

# Botão para selecionar arquivo via Dialog
botao_selecionar = tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.pack(pady=10)

root.mainloop()
