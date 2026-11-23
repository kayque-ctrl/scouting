"""Leitura dos arquivos brutos baixados do Kaggle."""

from pathlib import Path

import pandas as pd

# Raiz do projeto: este arquivo está em src/scouting/, então subimos 2 pastas
PASTA_RAIZ = Path(__file__).resolve().parents[2]
PASTA_BRUTOS = PASTA_RAIZ / "dados" / "brutos"
ARQUIVO_FBREF = PASTA_BRUTOS / "fbref" / "players_data-2024_2025.csv"

# Das 267 colunas do FBref, ficamos só com as que as análises usam.
# Chave = nome no FBref, valor = nosso nome em português.
COLUNAS_FBREF = {
    # Identificação
    "Player": "jogador",
    "Nation": "nacionalidade",
    "Pos": "posicao",
    "Squad": "clube",
    "Comp": "liga",
    "Born": "ano_nascimento",
    # Tempo de jogo
    "MP": "jogos",
    "Starts": "jogos_titular",
    "Min": "minutos",
    # Gols e finalização
    "Gls": "gols",
    "PK": "gols_penalti",
    "PKatt": "penaltis_cobrados",
    "xG": "xg",
    "npxG": "npxg",  # xG sem pênaltis
    "Sh": "finalizacoes",
    "SoT": "finalizacoes_no_alvo",
    # Criação
    "Ast": "assistencias",
    "xAG": "xag",  # xG dos chutes que vieram dos passes dele
    "xA": "xa",  # chance de cada passe virar assistência
    "KP": "passes_chave",
    "PPA": "passes_na_area",
    "SCA": "acoes_que_geram_chute",
    "GCA": "acoes_que_geram_gol",
    # Progressão com a bola
    "PrgP": "passes_progressivos",
    "PrgC": "conducoes_progressivas",
    "PrgR": "recepcoes_progressivas",
    "Succ": "dribles_certos",
    "Att_stats_possession": "dribles_tentados",
    "Touches": "toques",
    # Perdas e recuperações
    "Mis": "erros_de_dominio",
    "Dis": "desarmes_sofridos",
    "Recov": "recuperacoes",
    "Tkl+Int": "desarmes_e_interceptacoes",
    # Time com ele em campo
    "onG": "gols_time_em_campo",
    "onGA": "gols_sofridos_em_campo",
    "+/-90": "saldo_gols_por90_em_campo",
    "On-Off": "saldo_gols_on_off",  # saldo com ele menos saldo sem ele
    "onxG": "xg_time_em_campo",
    "onxGA": "xg_sofrido_em_campo",
    "xG+/-90": "saldo_xg_por90_em_campo",
}

COLUNAS_TEXTO = ["jogador", "nacionalidade", "posicao", "clube", "liga"]


def carregar_fbref(caminho: Path = ARQUIVO_FBREF) -> pd.DataFrame:
    """Lê o CSV do FBref, mantém só as colunas úteis e renomeia para português.

    Retorna uma linha por jogador por clube (quem trocou de clube na temporada
    aparece em mais de uma linha; isso é tratado no passo seguinte).
    """
    tabela = pd.read_csv(caminho, usecols=list(COLUNAS_FBREF))
    tabela = tabela.rename(columns=COLUNAS_FBREF)

    # Tudo que não é texto vira número; valor inválido vira vazio (NaN)
    colunas_numero = [c for c in tabela.columns if c not in COLUNAS_TEXTO]
    tabela[colunas_numero] = tabela[colunas_numero].apply(pd.to_numeric, errors="coerce")

    # "eng Premier League" -> "Premier League"
    tabela["liga"] = tabela["liga"].str.split(" ", n=1).str[1]

    return tabela[list(COLUNAS_FBREF.values())]
