from persistencia import carregar_dados, salvar_dados


ARQUIVO_JOGOS = "jogos.json"


def listar_jogos():
	"""Retorna a lista de jogos cadastrados."""
	return carregar_dados(ARQUIVO_JOGOS)


def cadastrar_jogo(nome, genero):
	"""Cadastra um jogo e retorna o registro criado."""
	jogos = listar_jogos()
	proximo_id = max((jogo.get("id", 0) for jogo in jogos), default=0) + 1
	jogo = {
		"id": proximo_id,
		"nome": nome.strip(),
		"genero": genero.strip(),
		"disponivel": True,
	}
	jogos.append(jogo)
	salvar_dados(ARQUIVO_JOGOS, jogos)
	return jogo


def buscar_jogo(id_jogo):
	"""Busca um jogo pelo identificador."""
	return next((jogo for jogo in listar_jogos() if jogo.get("id") == id_jogo), None)
