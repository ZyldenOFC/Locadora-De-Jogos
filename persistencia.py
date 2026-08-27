import json
from pathlib import Path


PASTA_DADOS = Path(__file__).parent


def carregar_dados(nome_arquivo):
	"""Carrega uma lista de registros de um arquivo JSON."""
	caminho = PASTA_DADOS / nome_arquivo
	if not caminho.exists():
		salvar_dados(nome_arquivo, [])
		return []

	try:
		with caminho.open("r", encoding="utf-8") as arquivo:
			dados = json.load(arquivo)
			return dados if isinstance(dados, list) else []
	except (json.JSONDecodeError, OSError):
		return []


def salvar_dados(nome_arquivo, dados):
	"""Salva registros no arquivo JSON com formatação legível."""
	caminho = PASTA_DADOS / nome_arquivo
	with caminho.open("w", encoding="utf-8") as arquivo:
		json.dump(dados, arquivo, ensure_ascii=False, indent=4)
