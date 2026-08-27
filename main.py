from clientes import cadastrar_cliente, listar_clientes
from jogos import cadastrar_jogo, listar_jogos
from locacoes import criar_locacao, finalizar_locacao, listar_locacoes


def mostrar_menu():
	print("\n=== GAME STOP ===")
	print("1 - Cadastrar cliente")
	print("2 - Cadastrar jogo")
	print("3 - Listar jogos")
	print("4 - Alugar jogo")
	print("5 - Devolver jogo")
	print("6 - Listar locacoes")
	print("0 - Sair")


def executar():
	while True:
		mostrar_menu()
		opcao = input("Escolha uma opcao: ").strip()

		try:
			if opcao == "1":
				nome = input("Nome: ")
				telefone = input("Telefone: ")
				print("Cliente cadastrado:", cadastrar_cliente(nome, telefone))
			elif opcao == "2":
				nome = input("Nome do jogo: ")
				genero = input("Genero: ")
				print("Jogo cadastrado:", cadastrar_jogo(nome, genero))
			elif opcao == "3":
				clientes = listar_clientes()
				locacoes = listar_locacoes()
				for jogo in listar_jogos():
					if jogo["disponivel"]:
						print(f'{jogo["id"]} - {jogo["nome"]} (Disponivel)')
						continue

					locacao_ativa = next(
						(
							locacao
							for locacao in locacoes
							if locacao.get("id_jogo") == jogo["id"]
							and locacao.get("ativa")
						),
						None,
					)
					cliente = next(
						(
							cliente
							for cliente in clientes
							if locacao_ativa
							and cliente.get("id") == locacao_ativa.get("id_cliente")
						),
						None,
					)
					if cliente:
						responsavel = f'{cliente["id"]} - {cliente["nome"]}'
					else:
						responsavel = "cliente nao identificado"
					print(f'{jogo["id"]} - {jogo["nome"]} (Alugado por: {responsavel})')
			elif opcao == "4":
				id_cliente = int(input("ID do cliente: "))
				id_jogo = int(input("ID do jogo: "))
				print("Locacao criada:", criar_locacao(id_cliente, id_jogo))
			elif opcao == "5":
				id_locacao = int(input("ID da locacao: "))
				dias = int(input("Quantos dias o jogo ficou alugado? "))
				locacao = finalizar_locacao(id_locacao, dias)
				print(
					f'Valor final: R$ {locacao["valor_final"]:.2f} '
					f'({locacao["desconto_percentual"]}% de desconto)'
				)
			elif opcao == "6":
				for locacao in listar_locacoes():
					print(locacao)
			elif opcao == "0":
				print("Ate logo!")
				break
			else:
				print("Opcao invalida.")
		except (ValueError, TypeError) as erro:
			print("Erro:", erro)


if __name__ == "__main__":
	executar()
