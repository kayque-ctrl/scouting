"""Leitura dos arquivos brutos baixados do Kaggle."""

from pathlib import Path

import pandas as pd

# Raiz do projeto: este arquivo está em src/scouting/, então subimos 2 pastas
PASTA_RAIZ = Path(__file__).resolve().parents[2]
PASTA_BRUTOS = PASTA_RAIZ / "dados" / "brutos"
ARQUIVO_FBREF = PASTA_BRUTOS / "fbref" / "players_data-2024_2025.csv"
PASTA_TM = PASTA_BRUTOS / "transfermarkt"

# As 14 ligas nacionais do Transfermarkt (as 5 grandes primeiro)
LIGAS_5_GRANDES = ["GB1", "ES1", "L1", "IT1", "FR1"]
LIGAS_NACIONAIS = LIGAS_5_GRANDES + [
    "PO1", "NL1", "BE1", "TR1", "RU1", "GR1", "SC1", "UKR1", "DK1",
]

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


def carregar_jogos_tm(pasta: Path = PASTA_TM) -> pd.DataFrame:
    """Jogos do Transfermarkt: de cada jogo, só a liga e a temporada oficial.

    A temporada vem do arquivo, não da data: na pandemia a 2019/20 terminou em
    agosto de 2020, e uma regra por data jogaria esses jogos na 2020/21.
    """
    jogos = pd.read_csv(pasta / "games.csv", usecols=["game_id", "competition_id", "season"])
    return jogos.rename(columns={"game_id": "id_jogo", "competition_id": "liga",
                                 "season": "temporada"})


def carregar_aparicoes_tm(pasta: Path = PASTA_TM) -> pd.DataFrame:
    """Cada linha é um jogador em um jogo (1,9 milhão de linhas)."""
    colunas = {
        "game_id": "id_jogo",
        "player_id": "id_jogador",
        "player_club_id": "id_clube",
        "minutes_played": "minutos",
        "goals": "gols",
        "assists": "assistencias",
    }
    aparicoes = pd.read_csv(pasta / "appearances.csv", usecols=list(colunas))
    return aparicoes.rename(columns=colunas)


def carregar_jogadores_tm(pasta: Path = PASTA_TM) -> pd.DataFrame:
    """Cadastro dos jogadores no Transfermarkt (1 linha por jogador)."""
    colunas = {
        "player_id": "id_jogador",
        "name": "nome",
        "date_of_birth": "data_nascimento",
        "country_of_citizenship": "nacionalidade",
        "position": "posicao_geral",
        "sub_position": "posicao_detalhada",
        "foot": "pe",
        "height_in_cm": "altura_cm",
        "current_club_name": "clube_atual",
        "current_club_domestic_competition_id": "liga_atual",
        "contract_expiration_date": "fim_contrato",
        "market_value_in_eur": "valor_atual_eur",
    }
    jogadores = pd.read_csv(pasta / "players.csv", usecols=list(colunas))
    jogadores = jogadores.rename(columns=colunas)
    for coluna in ["data_nascimento", "fim_contrato"]:
        jogadores[coluna] = pd.to_datetime(jogadores[coluna], errors="coerce")
    return jogadores
