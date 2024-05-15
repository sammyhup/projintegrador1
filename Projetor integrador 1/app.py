from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Caminho para o arquivo CSV
CSV_PATH = 'data/dados.csv'

# Contador de visualizações
visitas = 0

# Função para carregar dados do CSV
def carregar_dados():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        return pd.DataFrame(columns=['id', 'categoria', 'valor'])

# Função para salvar dados no CSV
def salvar_dados(dados):
    dados.to_csv(CSV_PATH, index=False)

@app.route('/')
def index():
    global visitas
    visitas += 1
    dados = carregar_dados()

    # Criar gráfico a partir dos dados
    grafico = px.bar(dados, x='categoria', y='valor', title='Gráfico de Pesquisa')

    # Salvar o gráfico em um arquivo HTML
    grafico_div = grafico.to_html(full_html=False)

    return render_template('index2.html', visitas=visitas, grafico_div=grafico_div, dados=dados.to_dict('records'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        dados = carregar_dados()
        novo_id = dados['id'].max() + 1 if not dados.empty else 1
        nova_entrada = {
            'id': novo_id,
            'categoria': request.form['categoria'],
            'valor': request.form['valor']
        }
        dados = dados.append(nova_entrada, ignore_index=True)
        salvar_dados(dados)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    dados = carregar_dados()
    entrada = dados[dados['id'] == id].iloc[0]

    if request.method == 'POST':
        dados.loc[dados['id'] == id, 'categoria'] = request.form['categoria']
        dados.loc[dados['id'] == id, 'valor'] = request.form['valor']
        salvar_dados(dados)
        return redirect(url_for('index'))
    
    return render_template('update.html', entrada=entrada)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        dados = carregar_dados()
        dados = dados[dados['id'] != id]
        salvar_dados(dados)
        return redirect(url_for('index'))
    
    return render_template('delete.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)
