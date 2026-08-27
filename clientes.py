from persistencia import carregar_dados, salvar_dados


ARQUIVO_CLIENTES = "clientes.json"


def listar_clientes():
	return carregar_dados(ARQUIVO_CLIENTES)


def cadastrar_cliente(nome, telefone):
	clientes = listar_clientes()
	proximo_id = max((cliente.get("id", 0) for cliente in clientes), default=0) + 1
	cliente = {"id": proximo_id, "nome": nome.strip(), "telefone": telefone.strip()}
	clientes.append(cliente)
	salvar_dados(ARQUIVO_CLIENTES, clientes)
	return cliente


def buscar_cliente(id_cliente):
	return next(
		(cliente for cliente in listar_clientes() if cliente.get("id") == id_cliente),
		None,
	)
