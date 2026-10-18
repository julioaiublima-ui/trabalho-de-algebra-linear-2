"""Simulador didatico de propagacao de influenza usando o modelo SIR."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


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


def salvar_csv(cenarios: dict[str, list[dict[str, float]]], caminho: Path) -> None:
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        campos = ["cenario", "dia", "suscetiveis", "infectados", "recuperados"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for nome, resultados in cenarios.items():
            for resultado in resultados:
                escritor.writerow({"cenario": nome, **resultado})


def salvar_grafico(cenarios: dict[str, list[dict[str, float]]], caminho: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as erro:
        raise RuntimeError("Instale matplotlib com: python3 -m pip install matplotlib") from erro

    cores = {"Base": "#d1495b", "Beta -25%": "#edae49", "Beta -50%": "#00798c"}
    figura, eixo = plt.subplots(figsize=(10, 6))
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
    figura.savefig(caminho, dpi=160)
    plt.close(figura)


def ler_numero(mensagem: str, padrao: float, conversao):
    resposta = input(f"{mensagem} [{padrao}]: ").strip().replace(",", ".")
    return padrao if not resposta else conversao(resposta)


def ler_parametros() -> Parametros:
    print("\nSimulador SIR de influenza - pressione Enter para usar o padrao.\n")
    populacao = ler_numero("Populacao", 1000, int)
    infectados = ler_numero("Infectados iniciais", 5, int)
    beta = ler_numero("Beta (taxa de transmissao)", 0.30, float)
    gamma = ler_numero("Gamma (taxa de recuperacao)", 0.10, float)
    duracao = ler_numero("Duracao em dias", 120, int)
    if populacao <= 0 or not 0 < infectados < populacao or beta < 0 or gamma < 0 or duracao <= 0:
        raise ValueError("Os parametros devem ser positivos e os infectados iniciais menores que a populacao.")
    return Parametros(populacao, infectados, beta, gamma, duracao)


def main() -> None:
    parametros = ler_parametros()
    cenarios = {
        "Base": simular(parametros),
        "Beta -25%": simular(parametros, parametros.beta * 0.75),
        "Beta -50%": simular(parametros, parametros.beta * 0.50),
    }
    for nome, resultados in cenarios.items():
        dia, valor = pico(resultados)
        print(f"{nome}: pico de {valor:.0f} infectados no dia {dia}.")

    pasta = Path(__file__).resolve().parent
    salvar_csv(cenarios, pasta / "resultados_simulacao.csv")
    salvar_grafico(cenarios, pasta / "graficos_simulacao.png")
    print("\nArquivos gerados: resultados_simulacao.csv e graficos_simulacao.png")


if __name__ == "__main__":
    main()