import sqlite3

def conectar():

    conn = sqlite3.connect("tsuzuku.db")

    conn.row_factory = sqlite3.Row

    return conn


def criar_tabelas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        email TEXT NOT NULL UNIQUE,

        senha TEXT NOT NULL

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS resumos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario_email TEXT NOT NULL,

        dispositivo TEXT,

        condicao TEXT,

        tempo_valor TEXT,

        tempo_unidade TEXT,

        multimedico TEXT,

        ano TEXT,

        status TEXT

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS exames (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario_email TEXT NOT NULL,

        nome_arquivo TEXT,

        tipo_arquivo TEXT,

        data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS importacoes (
                   

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario_email TEXT NOT NULL,

        dispositivo TEXT,

        condicao TEXT,

        tempo_valor TEXT,

        tempo_unidade TEXT,

        ano TEXT,

        status TEXT,

        origem TEXT,

        data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    

    """)

    conn.commit()

    conn.close()


def cadastrar_usuario(nome, email, senha):

    conn = conectar()

    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO usuarios (
            nome,
            email,
            senha
        )

        VALUES (?, ?, ?)

        """, (nome, email, senha))

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def buscar_usuario(email, senha):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM usuarios
    WHERE email = ? AND senha = ?

    """, (email, senha))

    usuario = cursor.fetchone()

    conn.close()

    return usuario

def salvar_resumo(usuario_email, dados):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO resumos (

        usuario_email,
        dispositivo,
        condicao,
        tempo_valor,
        tempo_unidade,
        multimedico,
        ano,
        status

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        usuario_email,
        dados["dispositivo"],
        dados["condicao"],
        dados["tempo_valor"],
        dados["tempo_unidade"],
        dados["multimedico"],
        dados["ano"],
        dados["status"]

    ))

    conn.commit()

    conn.close()


def buscar_ultimo_resumo(usuario_email):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM resumos

    WHERE usuario_email = ?

    ORDER BY id DESC

    LIMIT 1

    """, (usuario_email,))

    resumo = cursor.fetchone()

    conn.close()

    return resumo

def buscar_resumos_usuario(usuario_email):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM resumos

    WHERE usuario_email = ?

    ORDER BY id DESC

    """, (usuario_email,))

    resumos = cursor.fetchall()

    conn.close()

    return resumos

def salvar_importacao(usuario_email, dados):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO importacoes (

        usuario_email,
        dispositivo,
        condicao,
        tempo_valor,
        tempo_unidade,
        ano,
        status,
        origem

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        usuario_email,
        dados["dispositivo"],
        dados["condicao"],
        dados["tempo_valor"],
        dados["tempo_unidade"],
        dados["ano"],
        dados["status"],
        "QR Code"

    ))

    conn.commit()

    conn.close()
def popular_historico_teste(usuario_email):

    conn = conectar()

    cursor = conn.cursor()

    historico = [

        (
            usuario_email,
            "Fixador externo femoral",
            "Fratura múltipla após acidente automobilístico",
            "6",
            "meses",
            "Hospitalização",
            "2021",
            "Concluído"
        ),

        (
            usuario_email,
            "Prótese lombar",
            "Degeneração discal severa",
            "1",
            "ano",
            "Reabilitação",
            "2022",
            "Acompanhamento"
        ),

        (
            usuario_email,
            "Neuroestimulador medular",
            "Dor crônica neuropática",
            "2",
            "anos",
            "Controle da dor",
            "2023",
            "Ativo"
        ),

        (
            usuario_email,
            "Cateter venoso implantável",
            "Tratamento imunológico contínuo",
            "8",
            "meses",
            "Terapia",
            "2024",
            "Monitoramento"
        ),

        (
            usuario_email,
            "Órtese cervical",
            "Instabilidade cervical",
            "5",
            "meses",
            "Fisioterapia intensiva",
            "2025",
            "Recuperação"
        ),

        (
            usuario_email,
            "Marcapasso cardíaco",
            "Arritmia cardíaca persistente",
            "3",
            "anos",
            "Cardiologia",
            "2026",
            "Estável"
        )

    ]

    cursor.executemany("""

    INSERT INTO resumos (

        usuario_email,
        dispositivo,
        condicao,
        tempo_valor,
        tempo_unidade,
        multimedico,
        ano,
        status

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, historico)

    conn.commit()

    conn.close()

def salvar_exame(
    usuario_email,
    nome_arquivo,
    tipo_arquivo
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO exames (

        usuario_email,
        nome_arquivo,
        tipo_arquivo

    )

    VALUES (?, ?, ?)

    """, (

        usuario_email,
        nome_arquivo,
        tipo_arquivo

    ))

    conn.commit()

    conn.close()
    
def buscar_exames_usuario(usuario_email):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM exames

    WHERE usuario_email = ?

    ORDER BY id DESC

    """, (usuario_email,))

    exames = cursor.fetchall()

    conn.close()

    return exames

def excluir_exame(id_exame):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM exames

    WHERE id = ?

    """, (id_exame,))

    conn.commit()

    conn.close()