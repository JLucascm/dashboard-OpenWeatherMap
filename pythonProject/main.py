import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Função para obter dados meteorológicos
def obter_dados_meteorologicos(cidade, chave_api):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter dados: ", response.status_code)
        return None

# Substitua 'your_api_key' pela sua chave de API
chave_api = '4d608f5861e9767a1c75b33b65e92548'
cidade = 'São Paulo'

dados_meteorologicos = obter_dados_meteorologicos(cidade, chave_api)

# Verifique se os dados foram obtidos corretamente
if dados_meteorologicos:
    print(dados_meteorologicos)

    # Função para extrair os dados importantes
    def extrair_info_meteorologica(dados_meteorologicos):
        main = dados_meteorologicos['main']
        wind = dados_meteorologicos['wind']
        weather_desc = dados_meteorologicos['weather'][0]['description']

        dados = {
            'Temperatura': main['temp'],
            'Sensação Térmica': main['feels_like'],
            'Temperatura Mínima': main['temp_min'],
            'Temperatura Máxima': main['temp_max'],
            'Pressão': main['pressure'],
            'Umidade': main['humidity'],
            'Velocidade do Vento': wind['speed'],
            'Descrição': weather_desc.capitalize()  # Capitalizar a descrição do tempo
        }
        return dados

    # Extrair as informações
    info_meteorologica = extrair_info_meteorologica(dados_meteorologicos)
    print(info_meteorologica)  # Verificar se as informações foram extraídas corretamente

    # Criar um DataFrame
    df = pd.DataFrame([info_meteorologica])

    # Criar subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Temperatura", "Pressão e Umidade", "Velocidade do Vento", "Descrição"))

    # Adicionar gráfico de barras para a temperatura
    fig.add_trace(go.Bar(
        x=['Temperatura', 'Sensação Térmica', 'Temperatura Mínima', 'Temperatura Máxima'],
        y=[df['Temperatura'][0], df['Sensação Térmica'][0], df['Temperatura Mínima'][0], df['Temperatura Máxima'][0]],
        name='Temperatura',
        marker_color='indianred'
    ), row=1, col=1)

    # Adicionar gráfico de barras para pressão e umidade
    fig.add_trace(go.Bar(
        x=['Pressão', 'Umidade'],
        y=[df['Pressão'][0], df['Umidade'][0]],
        name='Pressão e Umidade',
        marker_color='lightsalmon'
    ), row=1, col=2)

    # Adicionar gráfico de barras para velocidade do vento
    fig.add_trace(go.Bar(
        x=['Velocidade do Vento'],
        y=[df['Velocidade do Vento'][0]],
        name='Velocidade do Vento',
        marker_color='lightblue'
    ), row=2, col=1)

    # Adicionar descrição do tempo
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        text=[df['Descrição'][0]],
        mode="text",
        showlegend=False
    ), row=2, col=2)

    # Atualizar layout
    fig.update_layout(
        title=f'Dados Meteorológicos para {cidade}',
        xaxis_title='Métrica',
        yaxis_title='Valor',
        height=700,
        showlegend=False
    )

    # Mostrar o gráfico
    fig.show()

    # Salvar o gráfico em um arquivo HTML
    fig.write_html('dashboard1.html')

    print("O dashboard foi salvo como 'dashboard.html'.")

else:
    print("Não foi possível obter os dados meteorológicos.")
