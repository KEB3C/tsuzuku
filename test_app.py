from app import app


# =====================================
# CONFIGURAÇÃO DE TESTE
# =====================================

app.config["TESTING"] = True

client = app.test_client()


# =====================================
# TESTE LANDING PAGE
# =====================================

def test_landing_page():

    response = client.get("/")

    assert response.status_code == 200


# =====================================
# TESTE LOGIN CORRETO
# =====================================

def test_login_sucesso():

    response = client.post("/login", data={

        "email": "teste@tsuzuku.com",
        "senha": "123456"

    }, follow_redirects=True)

    assert response.status_code == 200

    assert b"caso cl" in response.data.lower()


# =====================================
# TESTE LOGIN INVÁLIDO
# =====================================

def test_login_invalido():

    response = client.post("/login", data={

        "email": "errado@teste.com",
        "senha": "0000"

    }, follow_redirects=True)

    assert response.status_code == 200

    assert b"incorretos" in response.data.lower()


# =====================================
# TESTE ACESSO SEM LOGIN
# =====================================

def test_contexto_sem_login():

    with client.session_transaction() as sess:
        sess.clear()

    response = client.get("/contexto")

    assert response.status_code == 302


# =====================================
# TESTE FORMULÁRIO CLÍNICO
# =====================================

def test_envio_contexto():

    with client.session_transaction() as sess:
        sess["usuario"] = "teste@tsuzuku.com"

    response = client.post("/contexto", data={

        "dispositivo": "marcapasso",
        "condicao": "Dor no local do dispositivo",
        "tempo_valor": "3",
        "tempo_unidade": "anos",
        "multimedico": "sim",
        "ano": "2021",
        "status": "investigacao"

    }, follow_redirects=True)

    assert response.status_code == 200

    assert b"Resumo Cl" in response.data