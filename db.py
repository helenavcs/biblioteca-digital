import sqlite3

def conectar():
    return sqlite3.connect("catalogo.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano TEXT NOT NULL,
            genero TEXT NOT NULL,
            capa TEXT,
            pdf TEXT
        )
    """)
    conn.commit()
    conn.close()

def adicionar_livro(titulo, autor, ano, genero, capa, pdf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano, genero, capa, pdf)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, autor, ano, genero, capa, pdf))
    conn.commit()
    conn.close()

def listar_livros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return livros

def remover_livro(livro_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    conn.commit()
    conn.close()

def editar_livro(livro_id, titulo, autor, ano, genero, capa, pdf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE livros
        SET titulo=?, autor=?, ano=?, genero=?, capa=?, pdf=?
        WHERE id=?
    """, (titulo, autor, ano, genero, capa, pdf, livro_id))
    conn.commit()
    conn.close()
