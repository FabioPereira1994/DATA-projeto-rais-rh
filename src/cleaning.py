import pandas as pd
import numpy as np
import logging
from pathlib import Path
from ingestion import carregar_dados

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte as colunas para os tipos de dados corretos.
    """
    logger.info("Convertendo tipos de dados...")

    df["ANO"]               = pd.to_numeric(df["ANO"], errors="coerce").astype("Int64")
    df["IDADE"]             = pd.to_numeric(df["IDADE"], errors="coerce").astype("Int64")
    df["HORAS_CONTRATUAIS"] = pd.to_numeric(df["HORAS_CONTRATUAIS"], errors="coerce").astype("Int64")
    df["SALARIO_MENSAL"]    = pd.to_numeric(df["SALARIO_MENSAL"], errors="coerce")
    df["DATA_ADMISSAO"]     = pd.to_datetime(df["DATA_ADMISSAO"], errors="coerce")
    df["DATA_DESLIGAMENTO"] = pd.to_datetime(df["DATA_DESLIGAMENTO"], errors="coerce")

    colunas_texto = ["ID_VINCULO", "UF", "MUNICIPIO", "SETOR_ATIVIDADE",
                     "CARGO", "TIPO_VINCULO", "GENERO", "RACA_COR", "ESCOLARIDADE"]
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip().str.title()

    logger.info("Tipos convertidos com sucesso!")
    return df


def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores nulos de cada coluna.
    """
    logger.info("Tratando valores nulos...")

    # Salário: remove registros sem salário (não tem como imputar)
    antes = len(df)
    df = df[df["SALARIO_MENSAL"].notna()]
    logger.info(f"Removidos {antes - len(df)} registros sem salário")

    # Idade: preenche com a mediana
    mediana_idade = df["IDADE"].median()
    nulos_idade = df["IDADE"].isna().sum()
    df["IDADE"] = df["IDADE"].fillna(mediana_idade)
    logger.info(f"Idade: {nulos_idade} nulos preenchidos com mediana ({mediana_idade})")

    # Escolaridade: preenche com "Não Informado"
    nulos_esc = df["ESCOLARIDADE"].isna().sum()
    df["ESCOLARIDADE"] = df["ESCOLARIDADE"].fillna("Não Informado")
    logger.info(f"Escolaridade: {nulos_esc} nulos preenchidos com 'Não Informado'")

    # Data desligamento: nulo significa vínculo ativo — OK, mantém
    logger.info("Data desligamento: nulos mantidos (indicam vínculo ativo)")

    return df


def tratar_valores_invalidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove ou corrige registros com valores fora do domínio esperado.
    """
    logger.info("Tratando valores inválidos...")

    # Salário negativo ou zero
    antes = len(df)
    df = df[df["SALARIO_MENSAL"] > 0]
    logger.info(f"Removidos {antes - len(df)} registros com salário <= 0")

    # Idade inválida (0 ou acima de 100)
    antes = len(df)
    df = df[(df["IDADE"] >= 14) & (df["IDADE"] <= 100)]
    logger.info(f"Removidos {antes - len(df)} registros com idade inválida")

    # Data admissão no futuro
    antes = len(df)
    df = df[df["DATA_ADMISSAO"] <= pd.Timestamp("2022-12-31")]
    logger.info(f"Removidos {antes - len(df)} registros com data de admissão inválida")

    return df


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza valores categóricos e cria colunas derivadas úteis.
    """
    logger.info("Padronizando colunas e criando features...")

    # Coluna: situação do vínculo
    df["SITUACAO_VINCULO"] = df["DATA_DESLIGAMENTO"].apply(
        lambda x: "Desligado" if pd.notna(x) else "Ativo"
    )

    # Coluna: faixa etária
    bins   = [13, 24, 34, 44, 54, 64, 100]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    df["FAIXA_ETARIA"] = pd.cut(df["IDADE"], bins=bins, labels=labels)

    # Coluna: faixa salarial
    bins_sal   = [0, 1500, 3000, 6000, 12000, float("inf")]
    labels_sal = ["Até 1.5k", "1.5k-3k", "3k-6k", "6k-12k", "Acima 12k"]
    df["FAIXA_SALARIAL"] = pd.cut(df["SALARIO_MENSAL"], bins=bins_sal, labels=labels_sal)

    # Coluna: tempo de empresa em dias
    data_ref = pd.Timestamp("2022-12-31")
    df["TEMPO_EMPRESA_DIAS"] = df.apply(
        lambda row: (row["DATA_DESLIGAMENTO"] - row["DATA_ADMISSAO"]).days
        if pd.notna(row["DATA_DESLIGAMENTO"])
        else (data_ref - row["DATA_ADMISSAO"]).days,
        axis=1
    )

    logger.info("Padronização concluída!")
    return df


def salvar_dados(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame tratado em Excel na pasta processed.
    """
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False, sheet_name="RAIS_Tratado")
    logger.info(f"Dados tratados salvos em: {caminho}")


def resumo_limpeza(df: pd.DataFrame) -> None:
    """
    Exibe um resumo final após a limpeza.
    """
    print("\n" + "="*50)
    print("✅ RESUMO PÓS-LIMPEZA")
    print("="*50)
    print(f"\n📐 Dimensões finais: {df.shape[0]} linhas x {df.shape[1]} colunas")
    print(f"\n⚙️  Tipos de dados:")
    print(df.dtypes)
    print(f"\n❓ Valores nulos restantes:")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0] if nulos[nulos > 0].any() else "   Nenhum!")
    print(f"\n📊 Novas colunas criadas:")
    print(f"   - SITUACAO_VINCULO: {df['SITUACAO_VINCULO'].value_counts().to_dict()}")
    print(f"   - FAIXA_ETARIA:     {df['FAIXA_ETARIA'].value_counts().to_dict()}")
    print(f"   - FAIXA_SALARIAL:   {df['FAIXA_SALARIAL'].value_counts().to_dict()}")
    print("\n" + "="*50)


if __name__ == "__main__":
    CAMINHO_RAW       = "data/raw/RAIS_VINC_SP_2022_simulado.xlsx"
    CAMINHO_PROCESSED = "data/processed/RAIS_tratado.xlsx"

    df = carregar_dados(CAMINHO_RAW)
    df = converter_tipos(df)
    df = tratar_nulos(df)
    df = tratar_valores_invalidos(df)
    df = padronizar_colunas(df)
    resumo_limpeza(df)
    salvar_dados(df, CAMINHO_PROCESSED)