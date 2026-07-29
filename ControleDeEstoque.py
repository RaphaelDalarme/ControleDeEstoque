estoque = []
proximo_id = 1

def cadastrar_produto(nome, quantidade):
    global proximo_id

    novo_produto = {
        "id": proximo_id,
        "nome": nome,
        "quantidade": quantidade,
    }

    estoque.append(novo_produto)

    proximo_id += 1

    print(f"Produto {nome} cadastrado com sucesso!")

def dar_baixa_estoque(id_produto, quantidade):
    encontrado = False

    for produto in estoque:
        if produto["id"] == id_produto:
            encontrado = True

            if produto["quantidade"] < quantidade:
                print("Quantidade insuficiente em estoque para dar baixa.")
            else:
                produto["quantidade"] -= quantidade
                print(f"Baixa de {quantidade} unidades do produto {produto['nome']} realizada com sucesso!")

            break
    if not encontrado:
        print("Produto não encontrado no estoque.")

def adicionar_estoque(id_produto, quantidade):
    for produto in estoque:
        if produto["id"] == id_produto:
            produto["quantidade"] += quantidade
            print(f"Adição de {quantidade} unidades ao produto {produto['nome']} realizada com sucesso!")
            return

def excluir_produto(id_produto):
    global estoque
    for produto in estoque:
        if produto["id"] == id_produto:
            estoque.remove(produto)
            print(f"Produto {produto['nome']} excluído com sucesso!")
            break

def listar_produtos():
    if not estoque:
        print("Nenhum produto cadastrado no estoque.")
    else:
        print("Produtos cadastrados no estoque:")
        for produto in estoque:
            print(f"ID: {produto['id']}, Nome: {produto['nome']}, Quantidade: {produto['quantidade']}")

def conversor_de_numero(mensagem):
    while True:
        try:
            ler_inteiro = int(input(mensagem))
            return ler_inteiro
        except ValueError:
            print("Entrada inválida. Por favor, digite números inteiros.")

while True:

    print("Controle de Estoque")

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