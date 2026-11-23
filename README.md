# Renovar ou substituir?

**Uma ferramenta de decisão de contrato para clubes de futebol, baseada em dados.**

Quando o contrato de um meia ofensivo está perto de acabar, a diretoria faz uma pergunta: *renovar, ou existe alguém melhor ou mais barato no mercado?* Este projeto responde essa pergunta com dados reais. Ele traça o perfil do jogador, prevê o rendimento dele na próxima temporada, dá um veredito transparente e sugere substitutos parecidos. Tudo isso é contado num dashboard com storytelling: a temporada atual do jogador e o que esperar da próxima.

> 🚧 **Em construção.** A busca e a validação dos dados estão concluídas (fase 0). A análise, o modelo e o dashboard estão sendo construídos fase a fase. Veja o [roteiro](#roteiro).

---

## Como funciona

```
FBref 2024/25 ──────► Perfil do jogador: métricas por 90, percentis, radar
(5 grandes ligas)     Impacto no time com e sem ele, similaridade de estilo
                                      │
Transfermarkt ──────► Idade, valor de mercado, fim do contrato
(2012 → 2026)         Histórico de várias temporadas para treinar a previsão
                                      │
                                      ▼
                Previsão da próxima temporada (com faixa de incerteza)
                                      │
                                      ▼
        Veredito: RENOVAR / RENOVAR POR POUCO TEMPO / SUBSTITUIR
        + 5 alternativas parecidas, mais jovens ou mais baratas
                                      │
                                      ▼
        Dashboard com storytelling: a temporada atual → a previsão da próxima
```

A ferramenta funciona para **qualquer jogador** da base. O README vai contar um estudo de caso real do início ao fim: um meia ofensivo com contrato até junho de 2027.

## Princípios

- **Só dados reais.** Nenhum número simulado ou sintético.
- **Modelo honesto.** Todo modelo precisa ganhar de um baseline simples ("ele repete a última temporada"). A validação respeita o tempo: treina com temporadas antigas e testa nas mais novas, sem nunca embaralhar os anos. A previsão é uma faixa, não um número só.
- **Backtest.** O modelo prevê 2024/25 usando só dados até 2023/24, e a previsão é comparada com o que de fato aconteceu.
- **Veredito transparente.** A recomendação vem de critérios explícitos e explicáveis: nível, tendência, sustentabilidade da finalização (gols − xG), idade, disponibilidade e previsão. Não é um classificador caixa-preta, porque não existe um histórico rotulado de "renovações que deram certo" para treinar um.

## Roteiro

- [x] **0. Busca e validação dos dados**: fontes, licenças e cobertura conferidas
- [ ] **1. Preparação dos dados**: carregar, limpar, filtrar os meias ofensivos
- [ ] **2. Perfil do jogador**: métricas por 90, percentis contra os meias das 5 ligas, radar
- [ ] **3. Tendência**: primeiro contra segundo turno, evolução ao longo das temporadas
- [ ] **4. Gols contra xG**: qualidade ou sorte?
- [ ] **5. Impacto no time**: desempenho do time com e sem o jogador
- [ ] **6. Busca de substitutos**: similaridade de estilo nas 5 grandes ligas
- [ ] **7. Integração dos dados**: cruzar jogadores do FBref com o Transfermarkt
- [ ] **8. Previsão da próxima temporada**: baseline → linear → modelos mais complexos, com backtest
- [ ] **9. Veredito**: pontuação transparente
- [ ] **10. Dashboard com storytelling**: a história da temporada atual e da previsão para a próxima, para qualquer jogador
- [ ] **11. Estudo de caso**: análise completa de um jogador, relatório executivo de 1 página

## Dados

| Fonte | Conteúdo | Usado para |
|---|---|---|
| [Football Players Stats 2024-2025](https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025) (Kaggle, MIT) | 2.854 jogadores, 267 colunas, 5 grandes ligas: xG, xA, passes-chave, ações progressivas, SCA/GCA, dribles, ações defensivas, métricas com e sem o jogador em campo | Perfil do jogador, impacto no time, similaridade |
| [Transfermarkt dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores) (Kaggle, CC0) | Dados dos jogadores, fim de contrato, valores de mercado (2004–2026), jogos disputados partida a partida (2012–2026) | Modelo de previsão, tendência, idade, valor, contrato |

**Cobertura:** as 5 grandes ligas europeias. A temporada 2024/25 é a mais recente completa com métricas avançadas disponíveis publicamente, porque o FBref deixou de publicar as estatísticas avançadas da Opta em janeiro de 2026.

### Como baixar os dados

Os dados brutos não ficam neste repositório. Para baixá-los é preciso um [token da API do Kaggle](https://www.kaggle.com/settings), definido na variável de ambiente `KAGGLE_API_TOKEN`.

```bash
pip install kaggle

kaggle datasets download hubertsidorowicz/football-players-stats-2024-2025 \
  -f players_data-2024_2025.csv -p dados/brutos/fbref

for f in players.csv player_valuations.csv appearances.csv games.csv; do
  kaggle datasets download davidcariboo/player-scores -f $f -p dados/brutos/transfermarkt
done
```

> Observação: o código está em português (nomes de variáveis e funções, comentários). O README e os gráficos estão em inglês.

## Créditos

- Estatísticas dos jogadores: [FBref](https://fbref.com), com dados fornecidos pela Opta / Stats Perform. Base compilada no Kaggle por Hubert Sidorowicz.
- Valores de mercado, contratos e jogos: [Transfermarkt](https://www.transfermarkt.com). Base compilada por David Cariboo ([transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets)).
- Ideia do projeto inspirada num desafio de Jerry Strazzeri, ampliada com modelo de previsão e busca de substitutos.

## Autor

**Kayque Santos**: desenvolvedor de BI e dados, pós-graduando em IA, ML e Analytics.
