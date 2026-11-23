"""Histórico por temporada (Transfermarkt): a base de treino do modelo preditivo."""

import pandas as pd

from scouting.carregar import LIGAS_NACIONAIS

COLUNAS_SOMA = ["minutos", "gols", "assistencias"]


def montar_historico(aparicoes: pd.DataFrame, jogos: pd.DataFrame,
                     jogadores: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por jogador por temporada, só com jogos de liga nacional.

    - A temporada vem do jogo (coluna oficial), não da data.
    - Quem jogou em 2 ligas na mesma temporada tem os números somados; a liga
      e o clube principais são os de mais minutos.
    - Idade calculada em 1º de julho do ano de início da temporada.
    """
    # 1. Liga a cada aparição a liga e a temporada do jogo; fica só jogo de liga
    jogos_liga = jogos[jogos["liga"].isin(LIGAS_NACIONAIS)]
    tabela = aparicoes.merge(jogos_liga, on="id_jogo", how="inner")

    # 2. Soma por jogador, temporada, liga e clube (normalmente é 1 linha só)
    chave = ["id_jogador", "temporada"]
    por_clube = (tabela.groupby(chave + ["liga", "id_clube"], as_index=False)
                 .agg(jogos=("id_jogo", "count"), **{c: (c, "sum") for c in COLUNAS_SOMA}))

    # 3. Junta os clubes da mesma temporada; o principal é o de mais minutos
    por_clube = por_clube.sort_values("minutos", ascending=False)
    grupos = por_clube.groupby(chave, sort=False)
    historico = grupos[["jogos"] + COLUNAS_SOMA].sum()
    principal = grupos[["liga", "id_clube"]].first().rename(
        columns={"liga": "liga_principal", "id_clube": "id_clube_principal"})
    historico = principal.join(historico)
    historico["num_clubes"] = grupos["id_clube"].nunique()
    historico = historico.reset_index()

    # 4. Nome, posição e idade no início da temporada (1º de julho)
    cadastro = jogadores[["id_jogador", "nome", "data_nascimento", "posicao_detalhada"]]
    historico = historico.merge(cadastro, on="id_jogador", how="left")
    inicio_temporada = pd.to_datetime(historico["temporada"].astype(str) + "-07-01")
    historico["idade"] = (inicio_temporada - historico["data_nascimento"]).dt.days / 365.25
    historico["temporada_rotulo"] = (historico["temporada"].astype(str) + "/"
                                     + (historico["temporada"] + 1).astype(str).str[-2:])

    colunas = ["id_jogador", "nome", "temporada", "temporada_rotulo", "idade",
               "posicao_detalhada", "liga_principal", "id_clube_principal", "num_clubes",
               "jogos", "minutos", "gols", "assistencias"]
    return historico[colunas].sort_values(["id_jogador", "temporada"]).reset_index(drop=True)
