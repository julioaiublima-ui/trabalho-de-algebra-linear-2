from __future__ import annotations

from dataclasses import dataclass
import streamlit as st


@dataclass(frozen=True)
class Parametros:
    populacao: int = 1000
    infectados_iniciais: int = 5
    beta: float = 0.30
    gamma: float = 0.10
    duracao: int = 120


def simular(parametros: Parametros, beta: float | None = None) -> list[dict[str, float]]:
    """Executa o modelo SIR e registra o estado uma vez por dia."""
    taxa_transmissao = parametros.beta if beta is None else beta
    passos_por_dia = 10
    passo = 1 / passos_por_dia
    suscetiveis = float(parametros.populacao - parametros.infectados_iniciais)
    infectados = float(parametros.infectados_iniciais)
    recuperados = 0.0
    resultados = []

    for dia in range(parametros.duracao + 1):
        resultados.append(
            {
                "dia": dia,
                "suscetiveis": suscetiveis,
                "infectados": infectados,
                "recuperados": recuperados,
            }
        )
        for _ in range(passos_por_dia):
            novas_infeccoes = taxa_transmissao * suscetiveis * infectados / parametros.populacao
            novas_recuperacoes = parametros.gamma * infectados
            suscetiveis -= passo * novas_infeccoes
            infectados += passo * (novas_infeccoes - novas_recuperacoes)
            recuperados += passo * novas_recuperacoes

    return resultados


def pico(resultados: list[dict[str, float]]) -> tuple[int, float]:
    registro = max(resultados, key=lambda item: item["infectados"])
    return int(registro["dia"]), registro["infectados"]


# --- Interface do Web App (Streamlit) ---
st.title("Simulador SIR da Propagação de Influenza")
st.write("Disciplina: Álgebra Linear II - CIESA")
st.markdown("---")

# Controles deslizantes e entradas na barra lateral
st.sidebar.header("Parâmetros da Simulação")
populacao = st.sidebar.number_input("População", value=1000, step=100)
infectados_iniciais = st.sidebar.number_input("Infectados iniciais", value=5, step=1)
beta = st.sidebar.slider("Beta (taxa de transmissão)", min_value=0.05, max_value=1.0, value=0.30, step=0.01)
gamma = st.sidebar.slider("Gamma (taxa de recuperação)", min_value=0.01, max_value=0.5, value=0.10, step=0.01)
duracao = st.sidebar.slider("Duração em dias", min_value=30, max_value=240, value=120, step=10)

# Validação dos parâmetros
if populacao <= 0 or not 0 < infectados_iniciais < populacao or beta < 0 or gamma < 0 or duracao <= 0:
    st.error("Os parâmetros devem ser positivos e os infectados iniciais menores que a população.")
else:
    parametros = Parametros(populacao, infectados_iniciais, beta, gamma, duracao)
    
    # Execução dos cenários base e mitigação
    cenarios = {
        "Base": simular(parametros),
        "Beta -25%": simular(parametros, parametros.beta * 0.75),
        "Beta -50%": simular(parametros, parametros.beta * 0.50),
    }

    # Exibição rápida dos picos na tela
    st.subheader("Resultados dos Picos da Epidemia")
    col1, col2, col3 = st.columns(3)
    for i, (nome, resultados) in enumerate(cenarios.items()):
        dia, valor = pico(resultados)
        with [col1, col2, col3][i]:
            st.metric(label=nome, value=f"{valor:.0f} infectados", delta=f"Dia {dia}")

    st.markdown("---")

    # Geração do Gráfico Dinâmico no Web App
    st.subheader("Curvas Temporais de Infectados")
    try:
        import matplotlib.pyplot as plt
    except ImportError as erro:
        st.error("Instale matplotlib com: python3 -m pip install matplotlib")
        st.stop()

    cores = {"Base": "#d1495b", "Beta -25%": "#edae49", "Beta -50%": "#00798c"}
    figura, eixo = plt.subplots(figsize=(10, 5))
    
    for nome, resultados in cenarios.items():
        dias = [item["dia"] for item in resultados]
        infectados = [item["infectados"] for item in resultados]
        eixo.plot(dias, infectados, label=nome, linewidth=2.5, color=cores[nome])
        
    eixo.set_title("Simulacao SIR da propagacao de influenza")
    eixo.set_xlabel("Dias")
    eixo.set_ylabel("Pessoas infectadas")
    eixo.grid(alpha=0.25)
    eixo.legend()
    figura.tight_layout()
    
    st.pyplot(figura)