from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Contador de visualizações
visitas = 0

# Carregar os dados do CSV
dados = pd.read_csv('data/dados.csv')

@app.route('/')
def index():
    global visitas
    visitas += 1

    # Criar gráfico a partir dos dados
    grafico = px.bar(dados, x='Categoria', y='Valor', title='Gráfico de Pesquisa')

    # Salvar o gráfico em um arquivo HTML
    grafico_div = grafico.to_html(full_html=False)

    return render_template('index.html', visitas=visitas, grafico_div=grafico_div)

if __name__ == '__main__':
    app.run(debug=True)
