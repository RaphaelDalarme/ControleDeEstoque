import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "chave_secreta"

nome_banco = "estoque.db" 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Usuario(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, username FROM usuarios WHERE id = ?", (user_id,))
        usuario = cursor.fetchone()
        if usuario:
            return Usuario(id=usuario["id"], username=usuario["username"])
        return None

def conectar_banco():
    conexao = sqlite3.connect(nome_banco)
    conexao.row_factory = sqlite3.Row
    return conexao

def inicializar_banco():
    with conectar_banco() as conexao:
        cursor = conexao.cursor()

        # Tabela de Produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        if cursor.fetchone()["total"] == 0:
            senha_hash = generate_password_hash("admin123")
            cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", ("admin", senha_hash))
            print("Usuário padrão 'admin' criado com a senha 'admin123'.")

    print("Banco de dados inicializado com sucesso!")

inicializar_banco()

@app.route("/")
@login_required
def pagina_principal():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        with conectar_banco() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, username, senha FROM usuarios WHERE username = ?", (username,))
            usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario["senha"], senha):
            user = Usuario(id=usuario["id"], username=usuario["username"])
            login_user(user)
            return redirect(url_for("pagina_principal"))
        else:
            return render_template("login.html", erro="Credenciais inválidas.")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/produtos", methods=["GET"])
@login_required
def listar_produtos():
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, quantidade FROM produtos")
        linhas = cursor.fetchall()
        produtos = [dict(linha) for linha in linhas]
        return jsonify(produtos)

@app.route("/produtos", methods=["POST"])
@login_required
def cadastrar_produto():
    dados = request.get_json()

    if not dados or "nome" not in dados or "quantidade" not in dados:
        return jsonify({"erro": "Os campos 'nome' e 'quantidade' são obrigatórios."}), 400

    nome = dados["nome"]
    quantidade = dados["quantidade"]
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        novo_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO historico (produto_id, tipo, quantidade, data_hora) VALUES (?, ?, ?, ?)",
            (novo_id, "ENTRADA", quantidade, agora)
        )

        return jsonify({
            "id": novo_id,
            "nome": nome,
            "quantidade": quantidade,
            "mensagem": f"Produto '{nome}' cadastrado com sucesso!"
        }), 201

@app.route("/produtos/<int:id_produto>", methods=["DELETE"])
@login_required
def excluir_produto(id_produto):
    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        if cursor.rowcount > 0:
            return jsonify({"mensagem": f"Produto com ID {id_produto} excluído com sucesso!"}), 200
        else:
            return jsonify({"erro": f"Produto com ID {id_produto} não encontrado."}), 404

@app.route("/produtos/<int:id_produto>/adicionar", methods=["PUT"])
@login_required
def adicionar_estoque(id_produto):
    dados = request.get_json()

    if not dados or "quantidade" not in dados or dados["quantidade"] <= 0:
        return jsonify({"erro": "Informe uma quantidade válida para adicionar ao estoque."}), 400

    quantidade_adicionar = dados["quantidade"]
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade_adicionar, id_produto))

        if cursor.rowcount == 0:
            return jsonify({"erro": f"Produto com ID {id_produto} não encontrado."}), 404

        cursor.execute(
            "INSERT INTO historico (produto_id, tipo, quantidade, data_hora) VALUES (?, ?, ?, ?)",
            (id_produto, "ENTRADA", quantidade_adicionar, agora)
        )

        return jsonify({"mensagem": f"Adicionado {quantidade_adicionar} unidades ao produto com ID {id_produto}."}), 200

@app.route("/produtos/<int:id_produto>/baixar", methods=["PUT"])
@login_required
def dar_baixa_estoque(id_produto):
    dados = request.get_json()

    if not dados or "quantidade" not in dados or dados["quantidade"] <= 0:
        return jsonify({"erro": "Informe uma quantidade válida para dar baixa no estoque."}), 400

    quantidade_baixar = dados["quantidade"]
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conectar_banco() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT quantidade, nome FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            return jsonify({"erro": f"Produto com ID {id_produto} não encontrado."}), 404

        quantidade_atual = produto["quantidade"]

        if quantidade_baixar > quantidade_atual:
            return jsonify({"erro": "Quantidade a ser baixada é maior que a quantidade em estoque."}), 400

        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade_baixar, id_produto))

        cursor.execute(
            "INSERT INTO historico (produto_id, tipo, quantidade, data_hora) VALUES (?, ?, ?, ?)",
            (id_produto, "SAÍDA", quantidade_baixar, agora)
        )

        return jsonify({"mensagem": f"Baixado {quantidade_baixar} unidades do produto com ID {id_produto}."}), 200

@app.route("/api/dashboard", methods=["GET"])
@login_required
def obter_dados_dashboard():
    with conectar_banco() as conexao:
        query = """
            SELECT h.tipo, h.quantidade, p.nome
            FROM historico h
            JOIN produtos p ON h.produto_id = p.id
        """

        df = pd.read_sql_query(query, conexao)

        if df.empty:
            return jsonify({"entradas": {"labels": [], "valores": []}, "saidas": {"labels": [], "valores": []}}), 200

        # Filtra e agrupa no Pandas
        df_entradas = df[df["tipo"] == "ENTRADA"].groupby("nome")["quantidade"].sum().reset_index()
        df_saidas = df[df["tipo"] == "SAÍDA"].groupby("nome")["quantidade"].sum().reset_index()

        dados_resposta = {
            "entradas": {
                "labels": df_entradas["nome"].tolist(),
                "valores": df_entradas["quantidade"].tolist()
            },
            "saidas": {
                "labels": df_saidas["nome"].tolist(),
                "valores": df_saidas["quantidade"].tolist()
            }
        }
        return jsonify(dados_resposta), 200

if __name__ == "__main__":
    app.run(debug=True)