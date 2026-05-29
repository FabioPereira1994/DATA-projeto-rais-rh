import pandas as pd
import logging
from pathlib import Path

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Lê o arquivo Excel da RAIS e retorna um DataFrame bruto.
    Não realiza nenhuma transformação — apenas carrega e inspeciona.
    """
    path = Path(caminho)

    if not path.exists():
        logger.error(f"Arquivo não encontrado: {caminho}")
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    logger.info(f"Carregando arquivo: {path.name}")
    df = pd.read_excel(path, sheet_name="RAIS_Vinculos_2022", dtype=str)
    logger.info(f"Arquivo carregado com sucesso!")

    return df


def inspecionar_dados(df: pd.DataFrame) -> None:
    """
    Exibe informações iniciais sobre o DataFrame.
    """
    print("\n" + "="*50)
    print("📋 INSPEÇÃO INICIAL DOS DADOS")
    print("="*50)

    print(f"\n📐 Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")

    print(f"\n📌 Colunas disponíveis:")
    for col in df.columns:
        print(f"   - {col}")

    print(f"\n🔍 Primeiras 5 linhas:")
    print(df.head())

    print(f"\n⚙️  Tipos de dados:")
    print(df.dtypes)

    print(f"\n❓ Valores nulos por coluna:")
    nulos = df.isnull().sum()
    nulos_pct = (nulos / len(df) * 100).round(2)
    resumo_nulos = pd.DataFrame({"Nulos": nulos, "Percentual (%)": nulos_pct})
    print(resumo_nulos[resumo_nulos["Nulos"] > 0])

    print("\n" + "="*50)


if __name__ == "__main__":
    CAMINHO = "data/raw/RAIS_VINC_SP_2022_simulado.xlsx"

    df = carregar_dados(CAMINHO)
    inspecionar_dados(df)