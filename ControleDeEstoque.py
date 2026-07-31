import sqlite3

def inicializar_banco():
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)

    print("Banco de dados inicializado com sucesso!")

inicializar_banco()

def cadastrar_produto(nome, quantidade):
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
    print(f"Produto {nome} cadastrado com sucesso!")

def dar_baixa_estoque(id_produto, quantidade):
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()
        # Adicionado 'nome' na consulta para coincidir com o desempacotamento
        cursor.execute("SELECT quantidade, nome FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        
        if not produto:
            print(f"Produto com ID {id_produto} não encontrado.")
            return
            
        qta_atual, nome = produto

        if qta_atual < quantidade:
            print(f"Não é possível dar baixa de {quantidade} unidades de '{nome}'. Estoque atual: {qta_atual}.")
        else:
            cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, id_produto))
            print(f"Baixa de {quantidade} unidades do produto '{nome}' (ID {id_produto}) realizada com sucesso!")

def adicionar_estoque(id_produto, quantidade):
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, id_produto))
        if cursor.rowcount > 0:
            print(f"Adição de {quantidade} unidades ao produto com ID {id_produto} realizada com sucesso!")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")

def excluir_produto(id_produto):
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        if cursor.rowcount > 0:
            print(f"Produto com ID {id_produto} excluído com sucesso!")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")

def listar_produtos():
    with sqlite3.connect("estoque.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, quantidade FROM produtos")
        produtos = cursor.fetchall()
        
    if not produtos:
        print("Nenhum produto cadastrado no estoque.")
    else:
        print("Produtos cadastrados no estoque:")
        for produto in produtos:
            print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}")

def conversor_de_numero(mensagem):
    while True:
        try:
            ler_inteiro = int(input(mensagem))
            return ler_inteiro
        except ValueError:
            print("Entrada inválida. Por favor, digite números inteiros.")

while True:

    print("\nControle de Estoque")

    print("""Lista de comandos:
    1 - Cadastrar produto
    2 - Dar baixa em estoque
    3 - Adicionar ao estoque
    4 - Excluir produto
    5 - Listar produtos
    6 - Sair""")

    escolha = input("Digite o número do comando desejado: ")

    if escolha == "1":
        nome = input("Digite o nome do produto: ")
        quantidade = conversor_de_numero("Digite a quantidade do produto: ")
        cadastrar_produto(nome, quantidade)
    elif escolha == "2":
        id_produto = conversor_de_numero("Digite o ID do produto: ")
        quantidade = conversor_de_numero("Digite a quantidade a ser baixada: ")
        dar_baixa_estoque(id_produto, quantidade)
    elif escolha == "3":
        id_produto = conversor_de_numero("Digite o ID do produto: ")
        quantidade = conversor_de_numero("Digite a quantidade a ser adicionada: ")
        adicionar_estoque(id_produto, quantidade)
    elif escolha == "4":
        id_produto = conversor_de_numero("Digite o ID do produto: ")
        excluir_produto(id_produto)
    elif escolha == "5":
        listar_produtos()
    elif escolha == "6":
        print("Saindo do programa...")
        break 
    else:   
        print("Comando errado! Escolha novamente o comando desejado.")