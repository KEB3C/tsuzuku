from flask import send_from_directory
from flask import Flask, render_template, request, redirect, url_for, session
import os
from database import (
    criar_tabelas,
    cadastrar_usuario,
    buscar_usuario,
    salvar_resumo,
    buscar_ultimo_resumo,
    buscar_resumos_usuario,
    popular_historico_teste,
    salvar_exame,
    buscar_exames_usuario,
    excluir_exame
)
app = Flask(__name__)

# =====================================
# EXCLUIR EXAME
# =====================================

@app.route("/excluir_exame/<int:id_exame>")
def excluir_exame_route(id_exame):

    excluir_exame(id_exame)

    return redirect(url_for("exames"))

criar_tabelas()

# =====================================
# CONFIGURAÇÃO
# =====================================

app.secret_key = "tsuzuku_secret"

# usuário de teste
USER_EMAIL = "teste@tsuzuku.com"
USER_SENHA = "123456"


# =====================================
# LANDING PAGE
# =====================================

@app.route("/")
def landing():
    return render_template("landing.html")


# =====================================
# LOGIN
# =====================================

@app.route("/login", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:

            erro = "Preencha todos os campos."

        else:

            usuario = buscar_usuario(email, senha)

            if usuario:

                session["usuario"] = email

                return redirect(url_for("dashboard"))

            else:

                erro = "Email ou senha incorretos."

    return render_template(
        "login.html",
        erro=erro
    )

# =====================================
# DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("login"))

    resumo = buscar_ultimo_resumo(
        session["usuario"]
    )
    
    resumos = buscar_resumos_usuario(
    session["usuario"]
)

    return render_template(
    "dashboard.html",
    usuario=session["usuario"],
    resumo=resumo,
    resumos=resumos,
    pagina_ativa="dashboard"
)

# =====================================
# CADASTRO
# =====================================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    erro = None
    sucesso = None

    if request.method == "POST":

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        # validações
        if not nome or not email or not senha or not confirmar:

            erro = "Preencha todos os campos."

        elif senha != confirmar:

            erro = "As senhas não coincidem."

        else:

            usuario_criado = cadastrar_usuario(
                nome,
                email,
                senha
            )

            if usuario_criado:

                sucesso = "Conta criada com sucesso!"

            else:

                erro = "Este email já está cadastrado."

    return render_template(
        "cadastro.html",
        erro=erro,
        sucesso=sucesso
    )

# =====================================
# CONTEXTO CLÍNICO
# =====================================

@app.route("/contexto", methods=["GET", "POST"])
def contexto():

    # proteção de rota
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        dados = {

            "dispositivo": request.form.get("dispositivo"),

            "condicao": request.form.get("condicao"),

            "tempo_valor": request.form.get("tempo_valor"),

            "tempo_unidade": request.form.get("tempo_unidade"),

            "multimedico": request.form.get("multimedico"),

            "ano": request.form.get("ano"),

            "status": request.form.get("status")
        }

        # salva último resumo
        session["ultimo_resumo"] = dados

        salvar_resumo(
            session["usuario"],
            dados
        )

        return render_template(
            "resultado.html",
            dados=dados
        )

    return render_template("contexto.html")

# =====================================
# IMPORTAR QR
# =====================================

@app.route("/importar_qr", methods=["POST"])
def importar_qr():

    if "usuario" not in session:
        return {"erro":"não autenticado"}

    dados = request.json

    salvar_resumo(
        session["usuario"],
        dados
    )

    return {"sucesso":True}

# =====================================
# HISTÓRICO CLÍNICO
# =====================================

@app.route("/historico")
def historico():

    if "usuario" not in session:
        return redirect(url_for("login"))

    resumos = buscar_resumos_usuario(
        session["usuario"]
    )

    return render_template(
        "historico.html",
        resumos=resumos,
        pagina_ativa="historico"    
    )
# =====================================
# POPULAR HISTÓRICO TESTE
# =====================================

@app.route("/popular")
def popular():

    if "usuario" not in session:
        return redirect(url_for("login"))

    popular_historico_teste(
        session["usuario"]
    )

    return redirect(url_for("historico"))

# =====================================
# EXAMES E LAUDOS
# =====================================

@app.route("/exames", methods=["GET", "POST"])
def exames():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        arquivo = (

            request.files.get("arquivo_pdf")

            or request.files.get("arquivo_imagem")

            or request.files.get("arquivo_lab")

        )

        if arquivo:

            caminho = os.path.join(
                "uploads",
                arquivo.filename
            )

            arquivo.save(caminho)

            salvar_exame(

                session["usuario"],
                arquivo.filename,
                arquivo.content_type

            )

            return redirect(url_for("exames"))

    todos_exames = buscar_exames_usuario(
        session["usuario"]
    )

    pdfs = []
    imagens = []
    laboratoriais = []

    for exame in todos_exames:

        if "pdf" in exame["tipo_arquivo"]:

            pdfs.append(exame)

        elif "image" in exame["tipo_arquivo"]:

            imagens.append(exame)

        else:

            laboratoriais.append(exame)

    return render_template(
        "exames.html",
        pagina_ativa="exames",
        pdfs=pdfs,
        imagens=imagens,
        laboratoriais=laboratoriais
    )

# =====================================
# ABRIR EXAMES
# =====================================

@app.route("/uploads/<nome_arquivo>")
def abrir_exame(nome_arquivo):

    return send_from_directory(
        "uploads",
        nome_arquivo
    )

# =====================================
# LOGOUT
# =====================================

@app.route("/importar")
def importar():

    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template(
    "importar.html",
    pagina_ativa="importar"
)

@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("landing"))


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":
    app.run(debug=True)