# DATA-projeto-rais-rh
# Análise de Dados da RAIS/MTE com Python

Projeto de análise de dados reais do mercado de trabalho brasileiro,
utilizando a base pública da RAIS (Relação Anual de Informações Sociais).

## Objetivo
Extrair insights sobre emprego formal, salários e perfil dos trabalhadores
brasileiros a partir de dados reais do Ministério do Trabalho.

## Stack
- Python 3.10+
- Pandas
- Matplotlib / Seaborn
- python-pptx

## Estrutura do Projeto
- `data/raw/` → Dados originais (não versionados)
- `data/processed/` → Dados tratados
- `notebooks/` → Exploração e análise
- `src/` → Scripts modulares de ETL
- `output/presentation/` → Slides gerados

## Fonte dos Dados
RAIS - Ministério do Trabalho e Emprego
https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais

## Como Executar
1. Clone o repositório
2. Crie e ative o ambiente virtual
3. Instale as dependências: `pip install -r requirements.txt`
4. Baixe os dados da RAIS e coloque em `data/raw/`
5. Execute os scripts na ordem: ingestion → cleaning → analysis
