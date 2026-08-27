from datetime import date

from clientes import buscar_cliente
from jogos import buscar_jogo, listar_jogos
from persistencia import carregar_dados, salvar_dados


ARQUIVO_LOCACOES = "locacoes.json"
VALOR_DIA = 10.00


def calcular_desconto(dias):
	"""Retorna o percentual de desconto conforme os dias de locacao."""
	if dias <= 3:
		return 0
	if dias <= 7:
		return 5
	return 10


def calcular_valor(dias):
	desconto = calcular_desconto(dias)
	valor_bruto = VALOR_DIA * dias
	return round(valor_bruto * (1 - desconto / 100), 2)


def listar_locacoes():
	return carregar_dados(ARQUIVO_LOCACOES)


def criar_locacao(id_cliente, id_jogo):
	cliente = buscar_cliente(id_cliente)
	jogo = buscar_jogo(id_jogo)
	if cliente is None:
		raise ValueError("Cliente nao encontrado.")
	if jogo is None:
		raise ValueError("Jogo nao encontrado.")
	if not jogo.get("disponivel", False):
		raise ValueError("Este jogo ja esta alugado.")

	locacoes = listar_locacoes()
	proximo_id = max((locacao.get("id", 0) for locacao in locacoes), default=0) + 1
	locacao = {
		"id": proximo_id,
		"id_cliente": id_cliente,
		"id_jogo": id_jogo,
		"data_retirada": date.today().isoformat(),
		"data_devolucao": None,
		"dias": None,
		"desconto_percentual": None,
		"valor_final": None,
		"ativa": True,
	}
	locacoes.append(locacao)
	salvar_dados(ARQUIVO_LOCACOES, locacoes)

	jogos = listar_jogos()
	for item in jogos:
		if item.get("id") == id_jogo:
			item["disponivel"] = False
	salvar_dados("jogos.json", jogos)
	return locacao


def finalizar_locacao(id_locacao, dias):
	if dias < 0:
		raise ValueError("A quantidade de dias nao pode ser negativa.")

	locacoes = listar_locacoes()
	locacao = next((item for item in locacoes if item.get("id") == id_locacao), None)
	if locacao is None:
		raise ValueError("Locacao nao encontrada.")
	if not locacao.get("ativa"):
		raise ValueError("Esta locacao ja foi finalizada.")

	desconto = calcular_desconto(dias)
	locacao.update(
		{
			"data_devolucao": date.today().isoformat(),
			"dias": dias,
			"desconto_percentual": desconto,
			"valor_final": calcular_valor(dias),
			"ativa": False,
		}
	)
	salvar_dados(ARQUIVO_LOCACOES, locacoes)

	jogos = listar_jogos()
	for jogo in jogos:
		if jogo.get("id") == locacao.get("id_jogo"):
			jogo["disponivel"] = True
	salvar_dados("jogos.json", jogos)
	return locacao
