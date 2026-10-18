# Simulador de propagacao de influenza

Este projeto usa o modelo epidemiologico SIR para estudar, de forma hipotetica,
como a taxa de transmissao beta altera o numero de pessoas infectadas.

## Executar no macOS

```bash
python3 -m pip install -r requirements.txt
python3 simulador_influenza.py
```

Pressione `Enter` para aceitar os valores padrao. O programa compara a
transmissao original com reducoes de 25% e 50% e gera:

- `graficos_simulacao.png`: curvas de infectados para os tres cenarios;
- `resultados_simulacao.csv`: valores diarios de suscetiveis, infectados e recuperados.

Os valores representam uma simulacao matematica hipotetica, nao dados reais de
influenza. Para o trabalho, compare os picos ao variar beta e explique como a
taxa de transmissao muda as curvas.