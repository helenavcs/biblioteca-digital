import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import db
import os, subprocess, sys

class CatalogoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca Digital")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        largura = 900
        altura = 600
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")


        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.frame_catalogo = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.frame_catalogo, text="Catálogo")

        self.frame_cadastro = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.frame_cadastro, text="Cadastrar Livro")

        self.notebook.select(self.frame_catalogo)

        self.entry_titulo = self._criar_campo(self.frame_cadastro, "Título", 0)
        self.entry_autor = self._criar_campo(self.frame_cadastro, "Autor", 1)
        self.entry_ano = self._criar_campo(self.frame_cadastro, "Ano", 2)
        self.entry_genero = self._criar_campo(self.frame_cadastro, "Gênero", 3)

        tk.Label(self.frame_cadastro, text="Capa (PNG/GIF)", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
        tk.Button(self.frame_cadastro, text="Escolher Imagem", command=self.escolher_capa, bg="#d9ead3").grid(row=4, column=1, padx=5)
        self.caminho_capa = None
        self.lbl_capa_status = tk.Label(self.frame_cadastro, text="", bg="#f0f0f0")
        self.lbl_capa_status.grid(row=5, column=1, sticky="w")

        tk.Label(self.frame_cadastro, text="Arquivo PDF", bg="#f0f0f0").grid(row=6, column=0, sticky="w", pady=5)
        tk.Button(self.frame_cadastro, text="Escolher PDF", command=self.escolher_pdf, bg="#d9ead3").grid(row=6, column=1, padx=5)
        self.caminho_pdf = None
        self.lbl_pdf_status = tk.Label(self.frame_cadastro, text="", bg="#f0f0f0")
        self.lbl_pdf_status.grid(row=7, column=1, sticky="w")

        tk.Button(self.frame_cadastro, text="Adicionar Livro", command=self.adicionar, bg="#cfe2f3", font=("Arial", 10, "bold")).grid(row=8, column=1, pady=10)

        self.listar_catalogo()

    def _criar_campo(self, frame, texto, linha):
        tk.Label(frame, text=texto, bg="#f0f0f0").grid(row=linha, column=0, sticky="w", pady=5)
        entry = tk.Entry(frame, width=40)
        entry.grid(row=linha, column=1, pady=5)
        return entry

    def escolher_capa(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.gif")])
        if caminho:
            self.caminho_capa = caminho
            self.lbl_capa_status.config(text="Capa carregada com sucesso", fg="green")

    def escolher_pdf(self):
        caminho = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if caminho:
            self.caminho_pdf = caminho
            self.lbl_pdf_status.config(text="PDF carregado com sucesso", fg="green")

    def adicionar(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        ano = self.entry_ano.get()
        genero = self.entry_genero.get()

        if not titulo or not autor or not ano or not genero:
            messagebox.showwarning("Aviso", "Preencha todos os campos de texto!")
            return
        if not self.caminho_capa:
            messagebox.showwarning("Aviso", "Escolha uma imagem de capa (PNG/GIF)!")
            return
        if not self.caminho_pdf:
            messagebox.showwarning("Aviso", "Escolha um arquivo PDF!")
            return

        db.adicionar_livro(titulo, autor, ano, genero, self.caminho_capa, self.caminho_pdf)
        messagebox.showinfo("Sucesso", "Livro adicionado com capa e PDF!")

        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.caminho_capa = None
        self.caminho_pdf = None
        self.lbl_capa_status.config(text="")
        self.lbl_pdf_status.config(text="")

        self.listar_catalogo()

    def listar_catalogo(self):
        for widget in self.frame_catalogo.winfo_children():
            widget.destroy()

        livros = db.listar_livros()
        col, row = 0, 0
        for livro in livros:
            titulo, autor, ano, genero, capa, pdf = livro[1], livro[2], livro[3], livro[4], livro[5], livro[6]
            if capa:
                try:
                    img_tk = tk.PhotoImage(file=capa).subsample(4,4)
                    btn_img = tk.Button(self.frame_catalogo, image=img_tk, bg="#f0f0f0",
                                        command=lambda l=livro: self.mostrar_detalhes(l))
                    btn_img.image = img_tk
                    btn_img.grid(row=row, column=col, padx=10, pady=10)
                except:
                    tk.Label(self.frame_catalogo, text="[sem capa]", bg="#f0f0f0").grid(row=row, column=col, padx=10, pady=10)

            tk.Label(self.frame_catalogo, text=titulo, bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=row+1, column=col, padx=10, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 2

    def mostrar_detalhes(self, livro):
        titulo, autor, ano, genero, capa, pdf = livro[1], livro[2], livro[3], livro[4], livro[5], livro[6]

        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.configure(bg="#ffffff")

        largura = 500
        altura = 500
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

        tk.Label(janela, text=f"{titulo}\n{autor} ({ano}) - {genero}",
                 font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=10)

        if capa:
            try:
                img_tk = tk.PhotoImage(file=capa).subsample(2,2)
                lbl_img = tk.Label(janela, image=img_tk, bg="#ffffff")
                lbl_img.image = img_tk
                lbl_img.pack(pady=10)
            except:
                tk.Label(janela, text="[sem capa]", bg="#ffffff").pack(pady=10)

        if pdf:
            tk.Button(janela, text="Abrir PDF", command=lambda: self.abrir_pdf(pdf),
                      bg="#cfe2f3", font=("Arial", 10, "bold")).pack(pady=10)

        tk.Button(janela, text="Remover Livro",
                  command=lambda: self.remover_livro(livro[0], janela),
                  bg="#f4cccc", font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Button(janela, text="Editar Livro",
                  command=lambda: self.editar_livro(livro, janela),
                  bg="#fff2cc", font=("Arial", 10, "bold")).pack(pady=10)


    def remover_livro(self, livro_id, janela):
        if messagebox.askyesno("Confirmação", "Deseja realmente remover este livro?"):
            db.remover_livro(livro_id)
            messagebox.showinfo("Sucesso", "Livro removido com sucesso!")
            janela.destroy()
            self.listar_catalogo()


    def abrir_pdf(self, caminho_pdf):
        try:
            if sys.platform.startswith("win"):
                os.startfile(caminho_pdf)
            elif sys.platform.startswith("darwin"):
                subprocess.call(["open", caminho_pdf])
            else:
                subprocess.call(["xdg-open", caminho_pdf])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")


    def editar_livro(self, livro, janela_detalhes):
        livro_id, titulo, autor, ano, genero, capa, pdf = livro

        janela_edit = tk.Toplevel(self.root)
        janela_edit.title(f"Editar: {titulo}")
        janela_edit.configure(bg="#f9f9f9")

        largura = 500
        altura = 400
        largura_tela = janela_edit.winfo_screenwidth()
        altura_tela = janela_edit.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela_edit.geometry(f"{largura}x{altura}+{x}+{y}")

        entry_titulo = self._criar_campo(janela_edit, "Título", 0)
        entry_titulo.insert(0, titulo)

        entry_autor = self._criar_campo(janela_edit, "Autor", 1)
        entry_autor.insert(0, autor)

        entry_ano = self._criar_campo(janela_edit, "Ano", 2)
        entry_ano.insert(0, ano)

        entry_genero = self._criar_campo(janela_edit, "Gênero", 3)
        entry_genero.insert(0, genero)

        caminho_capa = capa
        tk.Button(janela_edit, text="Trocar Capa", command=lambda: self._trocar_arquivo("capa", janela_edit)).grid(row=4, column=1)

        caminho_pdf = pdf
        tk.Button(janela_edit, text="Trocar PDF", command=lambda: self._trocar_arquivo("pdf", janela_edit)).grid(row=5, column=1)

        def salvar():
            novo_titulo = entry_titulo.get()
            novo_autor = entry_autor.get()
            novo_ano = entry_ano.get()
            novo_genero = entry_genero.get()
            db.editar_livro(livro_id, novo_titulo, novo_autor, novo_ano, novo_genero, caminho_capa, caminho_pdf)
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            janela_edit.destroy()
            janela_detalhes.destroy()
            self.listar_catalogo()

        tk.Button(janela_edit, text="Salvar Alterações", command=salvar,
                  bg="#d9ead3", font=("Arial", 10, "bold")).grid(row=6, column=1, pady=10)
