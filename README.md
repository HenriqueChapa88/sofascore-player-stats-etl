# SofaScore Player Stats ETL

Projeto desenvolvido em Python para automatizar a extração, transformação e organização de estatísticas de jogadores de futebol a partir do SofaScore.

O objetivo foi criar um pipeline capaz de percorrer automaticamente as rodadas de uma temporada, identificar as partidas de uma determinada equipe, localizar um jogador específico e coletar suas principais métricas de desempenho.

Os dados obtidos são tratados e estruturados utilizando Pandas e posteriormente exportados para Excel, criando uma base pronta para análise de dados.

## 🚀 Funcionalidades

- Coleta automatizada das partidas de uma temporada
- Consumo de endpoints da API do SofaScore
- Identificação automática das partidas da equipe selecionada
- Busca do jogador nas escalações
- Extração de estatísticas individuais por partida
- Tratamento de dados ausentes
- Cálculo de métricas percentuais
- Consulta de diferentes endpoints da API
- Tratamento de erros e novas tentativas em caso de falha
- Organização dos dados utilizando Pandas
- Exportação automática para Excel

## 📊 Dados coletados

O pipeline coleta informações como:

- Data da partida
- Nota SofaScore
- Minutos jogados
- Gols
- Assistências
- Finalizações
- Passes certos
- Passes no campo adversário
- Passes no próprio campo
- Passes decisivos
- Cruzamentos
- Passes longos
- Ações com a bola
- Dribles
- Perdas de posse
- Faltas sofridas
- Faltas cometidas
- Desarmes
- Interceptações
- Cortes
- Recuperações de bola
- Duelos pelo chão
- Duelos pelo alto
- Cartões amarelos
- Cartões vermelhos

## 🔄 Pipeline de dados

O projeto segue um fluxo simplificado de ETL:

### Extract
Os dados são obtidos automaticamente através dos endpoints utilizados pelo SofaScore.

### Transform
Os dados em JSON são processados, tratados e transformados em informações estruturadas.

Também são calculadas métricas como precisão de passes, finalizações, cruzamentos, dribles, desarmes e duelos.

### Load
Após o processamento, os dados são organizados em um DataFrame Pandas e exportados para um arquivo Excel.

## 🛠️ Tecnologias utilizadas

- Python
- Pandas
- curl_cffi
- APIs REST
- JSON
- HTTP Requests
- Excel

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido como parte do meu Trabalho de Conclusão de Curso (TCC), voltado à análise da relação entre o desempenho de jogadores de futebol e os comentários publicados por torcedores nas redes sociais.

O objetivo desta etapa foi automatizar a coleta e a estruturação das estatísticas de desempenho dos jogadores no SofaScore, criando uma base de dados que pudesse ser posteriormente relacionada aos comentários coletados nas redes sociais.

Os dados obtidos foram utilizados em etapas posteriores de análise de sentimentos, mineração de dados e identificação de possíveis padrões entre o desempenho esportivo dos jogadores e a percepção dos torcedores.
