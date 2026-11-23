"""Limpeza das tabelas carregadas."""

import pandas as pd

# Colunas que são contagens: quem jogou em 2 clubes tem a soma das duas linhas
COLUNAS_SOMA = [
    "jogos", "jogos_titular", "minutos",
    "gols", "gols_penalti", "penaltis_cobrados", "xg", "npxg",
    "finalizacoes", "finalizacoes_no_alvo",
    "assistencias", "xag", "xa", "passes_chave", "passes_na_area",
    "acoes_que_geram_chute", "acoes_que_geram_gol",
    "passes_progressivos", "conducoes_progressivas", "recepcoes_progressivas",
    "dribles_certos", "dribles_tentados", "toques",
    "erros_de_dominio", "desarmes_sofridos", "recuperacoes", "desarmes_e_interceptacoes",
    "gols_time_em_campo", "gols_sofridos_em_campo",
    "xg_time_em_campo", "xg_sofrido_em_campo",
]


def _media_ponderada(valores: pd.Series, pesos: pd.Series) -> float:
    """Média em que cada valor pesa conforme seu peso (aqui, os minutos)."""
    validos = valores.notna() & (pesos > 0)
    if not validos.any():
        return float("nan")
    return (valores[validos] * pesos[validos]).sum() / pesos[validos].sum()


def juntar_trocas_de_clube(tabela: pd.DataFrame) -> pd.DataFrame:
    """Junta em uma linha só os jogadores que jogaram em mais de um clube na temporada.

    - Contagens (minutos, gols, xG...): somadas.
    - Saldos por 90 em campo: recalculados a partir das somas (conta exata).
    - On-off: média ponderada pelos minutos em cada clube. É uma aproximação,
      porque a conta exata precisaria dos dados do time sem ele em campo.
    - Clube, liga e posição: os do clube onde ele jogou mais minutos.
    """
    # Ordena por minutos para que a 1ª linha de cada jogador seja o clube principal
    tabela = tabela.sort_values("minutos", ascending=False)
    chave = ["jogador", "ano_nascimento"]
    grupos = tabela.groupby(chave, dropna=False, sort=False)

    juntos = grupos[COLUNAS_SOMA].sum()
    principal = grupos[["nacionalidade", "posicao", "clube", "liga"]].first()
    juntos = principal.join(juntos)
    juntos = juntos.rename(columns={"clube": "clube_principal", "liga": "liga_principal"})

    juntos["clubes"] = grupos["clube"].agg(" / ".join)
    juntos["num_clubes"] = grupos["clube"].count()

    # Saldo por 90 com ele em campo: (marcados - sofridos) / (minutos / 90)
    noventas = juntos["minutos"] / 90
    juntos["saldo_gols_por90_em_campo"] = (
        (juntos["gols_time_em_campo"] - juntos["gols_sofridos_em_campo"]) / noventas
    )
    juntos["saldo_xg_por90_em_campo"] = (
        (juntos["xg_time_em_campo"] - juntos["xg_sofrido_em_campo"]) / noventas
    )

    juntos["saldo_gols_on_off"] = grupos.apply(
        lambda g: _media_ponderada(g["saldo_gols_on_off"], g["minutos"]),
        include_groups=False,
    )

    return juntos.reset_index()
