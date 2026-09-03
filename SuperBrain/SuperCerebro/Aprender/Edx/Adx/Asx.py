import SuperBrain.SuperCerebro.Interpretacao.Edx.Adx.Ewx as iSupBrainInterpretacao

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Configuração de estilo para os gráficos
sns.set_theme(style="whitegrid")


def carregar_dicionario_em_pandas(dicionario: dict) -> pd.DataFrame:
    """
    Lê um dicionário e o converte para um DataFrame do pandas.
    """
    df = pd.DataFrame(dicionario)
    return df


def analisar_frequencia_dados(df: pd.DataFrame, coluna_alvo: str) -> dict:
    """
    Calcula a frequência dos dados, identifica a frequência mínima,
    a frequência máxima e os respectivos valores (números normais/categorias).
    """
    # Calcula a frequência de cada valor na coluna alvo
    serie_frequencia = df[coluna_alvo].value_counts()

    # Obtém os valores extremos de frequência
    freq_minima = serie_frequencia.min()
    freq_maxima = serie_frequencia.max()

    # Identifica quais valores (categorias) possuem essas frequências
    valores_freq_minima = serie_frequencia[serie_frequencia == freq_minima].index.tolist()
    valores_freq_maxima = serie_frequencia[serie_frequencia == freq_maxima].index.tolist()

    resultados = {
        "frequencia_total": serie_frequencia,
        "freq_minima": freq_minima,
        "valores_freq_minima": valores_freq_minima,
        "freq_maxima": freq_maxima,
        "valores_freq_maxima": valores_freq_maxima
    }

    return resultados


def executar_modelo_aprendizado_maquina(df: pd.DataFrame, colunas_features: list, coluna_target: str) -> dict:
    """
    Treina um modelo de aprendizado de máquina (KNN) utilizando dados reais.
    O modelo aprende com os dados de treino, é testado com dados de teste,
    e calcula as distâncias euclidianas para os vizinhos mais próximos.
    """
    # Preparação dos dados (Features e Target)
    X = df[colunas_features].values
    y = df[coluna_target].values

    # Mapeamento de categorias para números inteiros (exigido pelo scikit-learn)
    classes, y_encoded = np.unique(y, return_inverse=True)

    # Divisão em dados de treino (reais para aprendizado) e teste
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )

    # Inicialização e treinamento do modelo (K-Nearest Neighbors)
    modelo = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
    modelo.fit(X_treino, y_treino)

    # Previsões e cálculo de acurácia
    y_predito = modelo.predict(X_teste)
    acuracia = accuracy_score(y_teste, y_predito)

    # Cálculo das distâncias para os vizinhos mais próximos
    distancias, indices = modelo.kneighbors(X_teste)
    distancia_media = np.mean(distancias, axis=1)

    resultados_ml = {
        "X_teste": X_teste,
        "y_teste": y_teste,
        "y_predito": y_predito,
        "distancia_media": distancia_media,
        "acuracia": acuracia,
        "classes": classes
    }

    return resultados_ml


def visualizar_tudo_em_um_grafico(df: pd.DataFrame, resultados_freq: dict, resultados_ml: dict):
    """
    Plota a análise de frequência e os resultados do aprendizado de máquina
    (incluindo as distâncias calculadas) em uma única figura (janela gráfica).
    """
    fig, eixos = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Análise Integrada: Frequência de Dados e Aprendizado de Máquina (KNN)', fontsize=16,
                 fontweight='bold')

    # --- Gráfico 1: Análise de Frequência ---
    ax1 = eixos[0]
    freq_series = resultados_freq["frequencia_total"]
    sns.barplot(x=freq_series.index, y=freq_series.values, ax=ax1, palette="viridis")
    ax1.set_title('Distribuição de Frequência por Categoria', fontsize=12)
    ax1.set_xlabel('Categoria (Valor Normal)', fontsize=10)
    ax1.set_ylabel('Frequência Absoluta', fontsize=10)

    # Anotações para frequência mínima e máxima
    ax1.annotate(f'Máx: {resultados_freq["freq_maxima"]}',
                 xy=(resultados_freq["valores_freq_maxima"][0], resultados_freq["freq_maxima"]),
                 xytext=(0, 10), textcoords='offset points', ha='center', color='red', fontweight='bold')
    ax1.annotate(f'Mín: {resultados_freq["freq_minima"]}',
                 xy=(resultados_freq["valores_freq_minima"][0], resultados_freq["freq_minima"]),
                 xytext=(0, -15), textcoords='offset points', ha='center', color='blue', fontweight='bold')

    # --- Gráfico 2: Aprendizado de Máquina e Distâncias ---
    ax2 = eixos[1]
    X_teste = resultados_ml["X_teste"]
    y_teste = resultados_ml["y_teste"]
    y_predito = resultados_ml["y_predito"]
    distancias = resultados_ml["distancia_media"]

    # Mapeamento de cores para as classes reais
    cores_reais = np.array(['blue', 'green', 'orange'])[:len(np.unique(y_teste))]

    # Scatter plot onde o tamanho do ponto representa a distância calculada pelo modelo
    scatter = ax2.scatter(
        X_teste[:, 0], X_teste[:, 1],
        c=cores_reais[y_teste],
        s=distancias * 100,  # Escala do tamanho baseada na distância
        alpha=0.6,
        edgecolors='w',
        #s=distancias * 150,
        label='Dados de Teste (Tamanho = Distância)'
    )

    # Plotando as previsões com marcadores 'X' para comparação
    ax2.scatter(
        X_teste[:, 0], X_teste[:, 1],
        marker='x',
        c='red',
        s=50,
        label='Previsão do Modelo (Acurácia: {:.2f}%)'.format(resultados_ml["acuracia"] * 100)
    )

    ax2.set_title('Dispersão dos Dados e Distância Euclidiana (KNN)', fontsize=12)
    ax2.set_xlabel('Feature 1', fontsize=10)
    ax2.set_ylabel('Feature 2', fontsize=10)
    ax2.legend(loc='upper right', fontsize=9)

    plt.tight_layout()
    plt.show()


# ==============================================================================
# BLOCO DE EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    # 1. Dicionário de dados simulado
    dados_brutos = {
        'categoria': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'C', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'feature_1': [1.2, 2.3, 1.5, 3.1, 2.5, 1.1, 3.3, 3.0, 3.2, 2.4, 1.3, 3.4, 2.6, 1.4, 3.1],
        'feature_2': [2.1, 3.2, 2.4, 4.1, 3.5, 2.0, 4.3, 4.0, 4.2, 3.3, 2.2, 4.4, 3.6, 2.3, 4.1]
    }

    # 2. Leitura do dicionário para pandas
    dataframe = carregar_dicionario_em_pandas(dados_brutos)
    print("DataFrame carregado com sucesso:\n", dataframe.head(), "\n")

    # 3. Cálculo e análise de frequência
    analise_freq = analisar_frequencia_dados(dataframe, 'categoria')
    print("--- Análise de Frequência ---")
    print(f"Frequência Mínima: {analise_freq['freq_minima']} (Valor: {analise_freq['valores_freq_minima']})")
    print(f"Frequência Máxima: {analise_freq['freq_maxima']} (Valor: {analise_freq['valores_freq_maxima']})\n")

    # 4. Execução do modelo de aprendizado de máquina
    features = ['feature_1', 'feature_2']
    target = 'categoria'
    analise_ml = executar_modelo_aprendizado_maquina(dataframe, features, target)
    print("--- Aprendizado de Máquina ---")
    print(f"Acurácia do modelo no conjunto de teste: {analise_ml['acuracia'] * 100:.2f}%")
    print(f"Distância média calculada para os pontos de teste: {np.mean(analise_ml['distancia_media']):.4f}\n")

    # 5. Visualização gráfica unificada
    visualizar_tudo_em_um_grafico(dataframe, analise_freq, analise_ml)