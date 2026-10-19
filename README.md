# Simulador de Propagação de Influenza (Web App)

Este projeto, desenvolvido para a disciplina de Álgebra Linear II do CIESA, utiliza o modelo epidemiológico SIR para estudar a propagação da influenza através de um simulador matemático interativo em formato Web App.

## Como Executar Localmente

1. Certifique-se de ter o Python instalado e abra a pasta do projeto no terminal.
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   
Inicie o Web App com o Streamlit:

python -m streamlit run simulador_influenza.py

Funcionalidades do Simulador:

Interface Interativa: Altere parâmetros como população, infectados iniciais, taxa de transmissão (β), taxa de recuperação (γ) e duração em dias através de controles deslizantes (sliders). 

Análise de Cenários: Compara o cenário base com reduções de 25% e 50% na taxa de transmissão, simulando o efeito de medidas de controle.

Métricas e Gráficos Dinâmicos: Exibe o pico da epidemia em tempo real e plota as curvas temporais dos compartimentos SIR diretamente no navegador.

Os valores representam uma simulacao matematica hipotetica, nao dados reais de
influenza. Para o trabalho, compare os picos ao variar beta e explique como a
taxa de transmissao muda as curvas.
