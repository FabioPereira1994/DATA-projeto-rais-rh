import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Estilo global dos gráficos
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

OUTPUT_DIR = Path("output/presentation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def carregar_dados_tratados(caminho: str) -> pd.DataFrame:
    logger.info("Carregando dados tratados...")
    df = pd.read_excel(caminho)
    logger.info(f"Dados carregados: {df.shape[0]} registros")
    return df


def grafico_salario_por_setor(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: salário médio por setor...")
    media = (
        df.groupby("SETOR_ATIVIDADE")["SALARIO_MENSAL"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(media["SETOR_ATIVIDADE"], media["SALARIO_MENSAL"], color="#1F4E79")

    for bar in bars:
        ax.text(
            bar.get_width() + 80,
            bar.get_y() + bar.get_height() / 2,
            f"R$ {bar.get_width():,.0f}",
            va="center", fontsize=9
        )

    ax.set_title("Salário Médio Mensal por Setor de Atividade", fontweight="bold", pad=15)
    ax.set_xlabel("Salário Médio (R$)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.set_xlim(0, media["SALARIO_MENSAL"].max() * 1.2)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_salario_por_setor.png")
    plt.close()
    logger.info("Salvo: 01_salario_por_setor.png")


def grafico_distribuicao_genero(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: distribuição por gênero...")
    contagem = df["GENERO"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#1F4E79", "#A8C8E8"]
    wedges, texts, autotexts = ax.pie(
        contagem.values,
        labels=contagem.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for text in autotexts:
        text.set_fontsize(12)
        text.set_fontweight("bold")
        text.set_color("white")

    ax.set_title("Distribuição por Gênero", fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_distribuicao_genero.png")
    plt.close()
    logger.info("Salvo: 02_distribuicao_genero.png")


def grafico_escolaridade(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: distribuição por escolaridade...")
    ordem = [
        "Fundamental Incompleto", "Fundamental Completo",
        "Médio Incompleto", "Médio Completo",
        "Superior Incompleto", "Superior Completo",
        "Pós-Graduação", "Não Informado"
    ]
    contagem = (
        df["ESCOLARIDADE"]
        .value_counts()
        .reindex([o.title() for o in ordem])
        .dropna()
        .reset_index()
    )
    contagem.columns = ["ESCOLARIDADE", "TOTAL"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(contagem["ESCOLARIDADE"], contagem["TOTAL"], color="#1F4E79")

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            str(int(bar.get_height())),
            ha="center", va="bottom", fontsize=9
        )

    ax.set_title("Distribuição por Nível de Escolaridade", fontweight="bold", pad=15)
    ax.set_xlabel("")
    ax.set_ylabel("Quantidade de Vínculos")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_escolaridade.png")
    plt.close()
    logger.info("Salvo: 03_escolaridade.png")


def grafico_faixa_etaria(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: distribuição por faixa etária...")
    contagem = df["FAIXA_ETARIA"].value_counts().sort_index().reset_index()
    contagem.columns = ["FAIXA_ETARIA", "TOTAL"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(contagem["FAIXA_ETARIA"].astype(str), contagem["TOTAL"], color="#2E75B6")

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            str(int(bar.get_height())),
            ha="center", va="bottom", fontsize=9
        )

    ax.set_title("Distribuição por Faixa Etária", fontweight="bold", pad=15)
    ax.set_xlabel("Faixa Etária")
    ax.set_ylabel("Quantidade de Vínculos")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_faixa_etaria.png")
    plt.close()
    logger.info("Salvo: 04_faixa_etaria.png")


def grafico_salario_genero_setor(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: salário médio por gênero e setor...")
    media = (
        df.groupby(["SETOR_ATIVIDADE", "GENERO"])["SALARIO_MENSAL"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=media,
        y="SETOR_ATIVIDADE",
        x="SALARIO_MENSAL",
        hue="GENERO",
        palette={"Masculino": "#1F4E79", "Feminino": "#A8C8E8"},
        ax=ax
    )

    ax.set_title("Salário Médio por Gênero e Setor", fontweight="bold", pad=15)
    ax.set_xlabel("Salário Médio (R$)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.legend(title="Gênero")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_salario_genero_setor.png")
    plt.close()
    logger.info("Salvo: 05_salario_genero_setor.png")


def grafico_situacao_vinculo(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: situação dos vínculos...")
    contagem = df["SITUACAO_VINCULO"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#1F4E79", "#C00000"]
    wedges, texts, autotexts = ax.pie(
        contagem.values,
        labels=contagem.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for text in autotexts:
        text.set_fontsize(12)
        text.set_fontweight("bold")
        text.set_color("white")

    ax.set_title("Situação dos Vínculos Empregatícios", fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_situacao_vinculo.png")
    plt.close()
    logger.info("Salvo: 06_situacao_vinculo.png")


def grafico_top_cargos(df: pd.DataFrame) -> None:
    logger.info("Gerando gráfico: top 10 cargos...")
    top = df["CARGO"].value_counts().head(10).sort_values(ascending=True).reset_index()
    top.columns = ["CARGO", "TOTAL"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["CARGO"], top["TOTAL"], color="#2E75B6")

    for i, (val, _) in enumerate(zip(top["TOTAL"], top["CARGO"])):
        ax.text(val + 5, i, str(val), va="center", fontsize=9)

    ax.set_title("Top 10 Cargos Mais Frequentes", fontweight="bold", pad=15)
    ax.set_xlabel("Quantidade de Vínculos")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_top_cargos.png")
    plt.close()
    logger.info("Salvo: 07_top_cargos.png")


def imprimir_insights(df: pd.DataFrame) -> None:
    print("\n" + "="*55)
    print("💡 PRINCIPAIS INSIGHTS")
    print("="*55)

    print(f"\n💰 Salário médio geral: R$ {df['SALARIO_MENSAL'].mean():,.2f}")
    print(f"   Mediana salarial:    R$ {df['SALARIO_MENSAL'].median():,.2f}")
    print(f"   Maior salário:       R$ {df['SALARIO_MENSAL'].max():,.2f}")
    print(f"   Menor salário:       R$ {df['SALARIO_MENSAL'].min():,.2f}")

    top_setor = df.groupby("SETOR_ATIVIDADE")["SALARIO_MENSAL"].mean().idxmax()
    print(f"\n🏆 Setor com maior salário médio: {top_setor}")

    sal_masc = df[df["GENERO"] == "Masculino"]["SALARIO_MENSAL"].mean()
    sal_fem  = df[df["GENERO"] == "Feminino"]["SALARIO_MENSAL"].mean()
    gap = ((sal_masc - sal_fem) / sal_masc) * 100
    print(f"\n⚖️  Gap salarial de gênero:")
    print(f"   Masculino: R$ {sal_masc:,.2f}")
    print(f"   Feminino:  R$ {sal_fem:,.2f}")
    print(f"   Diferença: {gap:.1f}%")

    top_esc = df.groupby("ESCOLARIDADE")["SALARIO_MENSAL"].mean().idxmax()
    print(f"\n🎓 Escolaridade com maior salário médio: {top_esc}")

    ativos = df[df["SITUACAO_VINCULO"] == "Ativo"].shape[0]
    total  = df.shape[0]
    print(f"\n📋 Taxa de retenção: {ativos/total*100:.1f}% vínculos ativos")

    print("\n" + "="*55)


if __name__ == "__main__":
    CAMINHO = "data/processed/RAIS_tratado.xlsx"

    df = carregar_dados_tratados(CAMINHO)
    grafico_salario_por_setor(df)
    grafico_distribuicao_genero(df)
    grafico_escolaridade(df)
    grafico_faixa_etaria(df)
    grafico_salario_genero_setor(df)
    grafico_situacao_vinculo(df)
    grafico_top_cargos(df)
    imprimir_insights(df)
    logger.info("✅ Análise concluída! Gráficos salvos em output/presentation/")