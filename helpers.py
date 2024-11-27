import numpy as np
import pandas as pd
import base64, io
import os
from joblib import load   
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px


def text_intro():
    conteudo_inicio = html.Div([
        html.H4("Motivação"),
        html.P([
            "O ", 
            html.Strong("BigMart Sales"),
            " é um conjunto de dados desenvolvido pela ",
            html.A("analytics vidhya", href="https://datahack.analyticsvidhya.com/contest/practice-problem-big-mart-sales-iii/", target="_blank"),
            " para previsão de vendas a partir de produtos em diferentes lojas, com base em atributos informativos, como tamanho da loja, localização, tipo de produto, preço, promoções e descontos, entre outros. O desafio é construir um modelo de aprendizado de máquina que possa prever com precisão as vendas futuras com base nessas informações."
        ]),
        html.P([
            "Portanto, o desenvolvimento desse dashboard é motivado pelo desejo de tornar a previsão (e consequente análise e interpretação) dos dados mais acessível, útil e interativa para diferentes tipos de usuários."
        ]),

        html.H4("Geração de Hipóteses"),
        html.P("Para uma abordagem estruturada, com intuito de entender os fatores que mais impactam as vendas, as previsões geradas nesse dashboard tiveram como fundamento o seguinte conjunto de hipóteses:"),
        
        html.H5("Com base no item:"),
        html.Ul([
            html.Li([html.Strong("Visibilidade do item na loja:"), " A localização do produto dentro da loja pode impactar as vendas. Produtos localizados na entrada têm mais chances de chamar a atenção dos clientes do que aqueles posicionados no fundo da loja."]),
            html.Li([html.Strong("Frequência do produto:"), " Produtos mais populares (frequentemente comprados) tendem a apresentar vendas mais altas."]),
        ]),

        html.H5("Com base na loja:"),
        html.Ul([
            html.Li([html.Strong("Tipo de cidade:"), " Lojas localizadas em cidades urbanas devem ter vendas mais altas devido ao maior nível de renda dos moradores."]),
            html.Li([html.Strong("Capacidade da loja:"), " Lojas muito grandes devem apresentar vendas mais altas, pois funcionam como 'one-stop-shops' (lugares onde se encontra tudo em um só lugar), atraindo clientes que preferem fazer todas as compras em um único local."]),
        ]),

        html.H4("Sobre o Conjunto de Dados"),
        html.P([
            html.Strong("O Big Mart Sales"), 
            " é um conjunto de dados popular utilizado em problemas de previsão de vendas no varejo. Ele contém informações sobre vendas de produtos de 10 lojas da rede 'Big Mart', que estão localizadas em diferentes cidades e possuem diferentes tamanhos e tipos."
        ]),
        html.P("O conjunto de dados é composto por duas partes: A parte de treinamento contém informações sobre 8523 produtos, enquanto a parte de teste contém informações sobre 5681 produtos. Cada entrada no conjunto de dados contém informações sobre o identificador do produto, o identificador da loja, a localização da loja, o tipo de produto, o peso e o preço do produto, entre outras informações."),

        html.H5("Descrição dos atributos informativos:"),
        html.Ul([
            html.Li([html.Strong("Item_Weight:"), " Peso do produto ;", html.Strong(" (Não considerado nas hipóteses)")]),
            html.Li([html.Strong("Item_Fat_Content:"), " Se o produto é com baixo teor de gordura ou não;"]),
            html.Li([html.Strong("Item_Visibility:"), " A porcentagem da área total de exposição de todos os produtos em uma loja alocada para um produto específico;"]),
            html.Li([html.Strong("Item_Type:"), " O tipo de categoria que o produto pertence;"]),
            html.Li([html.Strong("Item_MRP:"), " Preço máximo de varejo (preço de lista) do produto;", html.Strong(" (Não considerado nas hipóteses)")]),
            html.Li([html.Strong("Outlet_Establishment_Year:"), " O ano em que a loja foi fundada;"]),
            html.Li([html.Strong("Outlet_Size:"), " O tamanho da loja em termos de área terrestre coberta;"]),
            html.Li([html.Strong("Outlet_Location_Type:"), " O tipo de cidade em que a loja está localizada;"]),
            html.Li([html.Strong("Outlet_Type:"), " Se a loja é apenas uma mercearia ou algum tipo de supermercado;"]),
        ]),

        html.P([
            html.Strong("Item_Outlet_Sales:"),
            " Representa as vendas totais de um produto específico em uma loja específica. Essa é o atributo alvo em que estamos interessados em prever no conjunto de dados."
        ]),
        html.P("O objetivo deste projeto é treinar um modelo de aprendizagem supervisionada para estimar com precisão as vendas futuras e com isso entender quais produtos e lojas causam mais impacto no crescimento das vendas. Por meio da biblioteca Dash Python foi possível criar uma aplicação web interativa e personalizada para visualização e análise do Big Mart Sales Prediction Dataset. De forma a explorar os dados de forma dinâmica, fazer previsões e compartilhar insights de forma fácil e interativa."),

        html.H4("Código GitHub"),
        html.P([
            "Interessado no desenvolvimento do projeto? ",
            html.A("Clique aqui para ver o código fonte!", href="https://github.com/wanderson42/bigmart_dash_app.git", target="_blank"),
            " Para ter acesso ao projeto na íntegra, que contempla desde uma minuciosa análise de dados, bem como o treinamento de um modelo random forest confiável para previsão de vendas, e não menos importante a construção desta aplicação web."
        ])
    ])
    return conteudo_inicio

# Função para criar menu suspenso de categorias da página "Previsões Individuais"
def create_dropdown(feature, searchable=False):
    """
    Cria um menu suspenso (dropdown) personalizado para Dash.
    
    :param feature: Nome da feature para o dropdown.
    :param options: Lista de opções disponíveis para o dropdown.
                    Se None, será usado o dicionário padrão `categorias`.
    :return: Elemento HTML contendo o dropdown.
    """    
    # Dicionários com as categorias para as features discretas da página "Previsões"
    categorias = {
        "Outlet_Identifier": ['OUT010', 'OUT013',  'OUT017', 'OUT018', 'OUT019',  'OUT027', 'OUT035', 'OUT045',  'OUT046', 'OUT049'],  # Atualizado com as categorias corretas        
        "Item_Reference": ['Food', 'Drinks', 'Non-Consumable'],
        "Item_Fat_Content": ['Low_Fat', 'Regular', 'Inedible'],  # Atualizado com as categorias corretas
        "Item_Type": ['Canned', 'Household', 'Hard_Drinks', 'Health_and_Hygiene',
        'Frozen_Foods', 'Baking_Goods', 'Fruits_and_Vegetables',
        'Snack_Foods', 'Dairy', 'Meat', 'Breakfast', 'Others',
        'Starchy_Foods', 'Soft_Drinks', 'Seafood', 'Breads'],  # Atualizado com as categorias corretas
        "Outlet_Size": ['Small', 'Medium',  'High'],  # Atualizado com as categorias corretas
        "Outlet_Location_Type": ['Tier_1', 'Tier_2', 'Tier_3'],  # Atualizado com as categorias corretas
        "Outlet_Type": ['Grocery_Store', 'Supermarket_Type1', 'Supermarket_Type2']  # Atualizado com as categorias corretas
    }

    return html.Div([
        html.H6(f"{feature}:"),
        dcc.Dropdown(
            id=f'dropdown-{feature}',
            options=[] if searchable else [{'label': i, 'value': i} for i in categorias.get(feature, [])],
            placeholder=f"Digite ou selecione {feature}...",
            multi=False, # Configurar para múltiplas seleções se necessário
            searchable=searchable, # Permitir busca digitando
            style={"width": "180px"} if searchable else {"width": "180px"}
        ),
    ])

# função para processar o arquivo .csv após o upload e exibi-lo em uma tabela de dados no callback:
def read_uploaded_data(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    loaded_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return loaded_data

def parse_contents(contents):
    loaded_data = read_uploaded_data(contents)

    return html.Div([
        html.H5('Dados do arquivo .csv:'),
        dash_table.DataTable(
            data=loaded_data.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in loaded_data.columns],
            style_table={'height': '300px', 'overflowY': 'auto', 'position': 'relative'},
        ),
        html.Button('Fazer Previsões', id='submit-button', n_clicks=0, style={
            'background-color': '#f1863d',
            'border-radius': '5px',
            'padding': '5px',
            'color': 'black',
            'bottom': '5px',
        }),
    ], style={'width': '100%', 'position': 'relative'})


# Função para fazer previsões com base nas entradas do usuário.
def make_predictions(user_data):
    '''
    Faz previsões de vendas com base nos dados fornecidos pelo usuário.

    Esta função utiliza um modelo de regressão linear previamente treinado para 
    prever valores de vendas, permitindo entradas de dados em formato de dicionário (uma única previsão) 
    ou DataFrame (previsões em lote). O modelo foi treinado para trabalhar com features numéricas e categóricas,
    e pode inferir informações adicionais com base no identificador da loja ('Outlet_Identifier').

    Retorno:
    -------
    numpy.ndarray
        Um array contendo os valores previstos (em sua escala original).

    Exceções:
    ---------
    ValueError:
        - Caso o 'Outlet_Identifier' esteja ausente ou seja desconhecido no dicionário de entrada.
        - Caso o DataFrame ou dicionário fornecido não possua as colunas esperadas pelo modelo.

    '''
    # Caminho para o modelo treinado
    location = os.getcwd()
    path_model = os.path.join(location, 'Linear_Regression_best_model.pkl')
    lr_model = load(path_model)

    # Se for uma previsão individual o input sera um dicionário:
    if isinstance(user_data, dict):

      # Dicionário para inferência de diversos atributos baseada em 'Outlet_Identifier'
      outlet_info = {
          'OUT010': {'Outlet_Type': 'Grocery_Store', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_3', 'Outlet_Years': 25},
          'OUT013': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'High', 'Outlet_Location_Type': 'Tier_3', 'Outlet_Years': 36},
          'OUT017': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_2', 'Outlet_Years': 16},
          'OUT018': {'Outlet_Type': 'Supermarket_Type2', 'Outlet_Size': 'Medium', 'Outlet_Location_Type': 'Tier_3', 'Outlet_Years': 14},
          'OUT019': {'Outlet_Type': 'Grocery_Store', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_1', 'Outlet_Years': 38},
          'OUT027': {'Outlet_Type': 'Supermarket_Type3', 'Outlet_Size': 'Medium', 'Outlet_Location_Type': 'Tier_3', 'Outlet_Years': 38},
          'OUT035': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_2', 'Outlet_Years': 19},
          'OUT045': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_2', 'Outlet_Years': 21},
          'OUT046': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'Small', 'Outlet_Location_Type': 'Tier_1', 'Outlet_Years': 26},
          'OUT049': {'Outlet_Type': 'Supermarket_Type1', 'Outlet_Size': 'Medium', 'Outlet_Location_Type': 'Tier_1', 'Outlet_Years': 24}
      }

      # Verificar se 'Outlet_Identifier' está presente nos dados do usuário
      if 'Outlet_Identifier' not in user_data:
          raise ValueError("Missing 'Outlet_Identifier' in user data.")

      outlet_identifier = user_data['Outlet_Identifier']
      if outlet_identifier not in outlet_info:
          raise ValueError(f"Unknown Outlet Identifier: {outlet_identifier}")

      # Combinar os dois dicionários
      combined_data = {**user_data, **outlet_info[outlet_identifier]}

      # Garantir que valores numéricos estejam encapsulados em listas
      num_features = ['Item_Visibility', 'Item_MRP', 'Outlet_Years']
      for feature in num_features:
          if feature in combined_data and not isinstance(combined_data[feature], list):
              combined_data[feature] = [combined_data[feature]]

      # Converter dicionário combinado para DataFrame
      user_data = pd.DataFrame.from_dict(combined_data)

    # Verificar colunas esperadas pelo modelo
    expected_columns = lr_model.feature_names_in_

    # Ordenar as colunas na ordem esperada
    user_data = user_data[expected_columns]

    # Fazer previsão
    predictions = np.square(lr_model.predict(user_data))

    return predictions


# Apartir daqui são as funções de plot 

# Paleta de Cores
CATEGORY_COLORS = {
    'Fruits_and_Vegetables': '#1f77b4',  # Azul vibrante
    'Snack_Foods': '#ff7f0e',            # Laranja vibrante
    'Household': '#2ca02c',              # Verde forte
    'Frozen_Foods': '#d62728',           # Vermelho escuro
    'Dairy': '#9467bd',                  # Roxo suave
    'Canned': '#8c564b',                 # Marrom suave
    'Soft_Drinks': '#e377c2',            # Rosa claro
    'Meat': '#7f7f7f',                   # Cinza médio
    'Baking_Goods': '#bcbd22',           # Amarelo forte
    'Health_and_Hygiene': '#17becf',     # Azul claro
    'Starchy_Foods': '#ff9896',          # Rosa claro
    'Breakfast': '#c5b0d5',              # Lilás suave
    'Hard_Drinks': '#aec7e8',            # Azul suave
    'Seafood': '#ffbb78',                # Laranja claro
    'Breads': '#98df8a',                 # Verde claro
    'Others': '#c7c7c7',                 # Cinza claro
    'Supermarket_Type1': '#FF5733',      # Vermelho alaranjado vibrante
    'Supermarket_Type2': '#2E8B57',      # Verde médio
    'Supermarket_Type3': '#482344',      # Violeta
    'Grocery_Store': '#1E90FF',          # Azul vibrante
}


def assign_colors(df, category_col):
    """
    Garante que todas as categorias no DataFrame tenham uma cor atribuída fixa.
    Se alguma categoria não estiver no mapeamento, levanta um aviso ou atribui uma cor padrão fixa.
    """
    global CATEGORY_COLORS

    # Verificar categorias presentes no DataFrame
    categories_in_data = set(df[category_col].unique())

    # Identificar categorias que não possuem cores atribuídas
    missing_categories = categories_in_data - set(CATEGORY_COLORS.keys())

    # Levantar exceção ou logar categorias ausentes
    if missing_categories:
        raise ValueError(f"As seguintes categorias não têm cores atribuídas: {missing_categories}")

    # Retornar um mapa de cores para as categorias presentes no DataFrame
    return {cat: CATEGORY_COLORS[cat] for cat in categories_in_data}



def plotly_sales_by_category(df):
    # Calculando as porcentagens de vendas
    total_sales = df['Item_Outlet_Sales'].sum()
    df['Sales Percentage'] = df['Item_Outlet_Sales'] / total_sales * 100

    # Ordenando as categorias por porcentagem de vendas
    df = df.sort_values('Sales Percentage', ascending=False)

    # Garantir que todas as categorias têm cores atribuídas
    assign_colors(df, 'Item_Type')

    # Criando um gráfico de anel (donut chart)
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=df['Item_Type'],
        values=df['Sales Percentage'],
        hole=0.7,  # Tamanho do buraco no meio do anel
        textinfo='percent',
        insidetextfont=dict(color='black'),  # Cor do texto dentro das fatias
        marker=dict(colors=[CATEGORY_COLORS[cat] for cat in df['Item_Type']],
                    line=dict(color='white', width=2)),  # Aplicar cores consistentes
    ))

    fig.update_traces(hole=0.6)  # Define o tamanho uniforme para o anel

    # Adicionando uma imagem dentro do buraco da pizza
    fig.add_layout_image(
        source="https://raw.githubusercontent.com/wanderson42/bigmart_dash_app/main/264-2640171_inventory-icon-white.png",
        x=0.5, y=0.5, xanchor="center", yanchor="middle", sizex=0.4, sizey=0.4
    )

    fig.update_layout(
        title='Distribuição de Vendas por Tipo de Produto',
        title_x=0.15,
        title_font=dict(color='black', size=20),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.2),
        margin=dict(t=50),
    )

    return fig


# @title
def plotly_sales_over_outlet(df, top_n=10):
    # Agrupar as features com a previsão
    sales_by_category = df.groupby(['Item_Type', 'Outlet_Identifier', 'Outlet_Size', 'Outlet_Location_Type']).agg(
        {'Item_Outlet_Sales': 'sum', 'Item_Type': 'count'}).rename(columns={'Item_Type': 'Item_Count'}).reset_index()

    # Garantir que todas as categorias têm cores atribuídas
    assign_colors(sales_by_category, 'Item_Type')

    # Calcular a soma total de vendas para cada tipo de produto
    total_sales_by_item = sales_by_category.groupby('Item_Type')['Item_Outlet_Sales'].sum().reset_index()
    total_sales_by_item = total_sales_by_item.sort_values(by='Item_Outlet_Sales', ascending=False)
    sorted_item_types = total_sales_by_item['Item_Type'].tolist()

    # Filtrar para incluir apenas os top 10 produtos mais vendidos em cada tipo de loja
    top_items = (
        sales_by_category
        .sort_values(by='Item_Outlet_Sales', ascending=False)
        .groupby('Outlet_Identifier')
        .head(top_n)
    )

    # Gráfico de barras agrupadas para cada produto em função das lojas
    fig_bar_grouped = px.bar(
        top_items,
        x='Outlet_Identifier',
        y='Item_Outlet_Sales',
        color='Item_Type',
        text='Item_Count',  # Adiciona o texto direto no trace (mais confiável)
        title=f'Top {top_n} Produtos Mais Vendidos por Loja',
        labels={'Item_Outlet_Sales': 'Item_Outlet_Sales', 'Outlet_Identifier': 'Outlet_Identifier'},
        category_orders={'Item_Type': sorted_item_types},
        barmode='group',  # Define o modo de barras agrupadas
        color_discrete_map=CATEGORY_COLORS  # Aplicar cores consistentes
    )

    # Atualizar o layout para exibir os números dentro das barras
    fig_bar_grouped.update_traces(
        textposition='inside',  # Garante que o texto fique dentro das barras
        texttemplate='%{text}',  # Formata o texto (quantidade de itens vendidos)
        textfont=dict(size=88),  # Aumenta o tamanho do texto dentro das barras
        marker=dict(line=dict(color='white', width=1))  # Bordas brancas nas barras
    )

    # Adicionar anotações de Outlet_Size e Outlet_Location_Type no eixo X
    outlet_info_map = sales_by_category[['Outlet_Identifier', 'Outlet_Size', 'Outlet_Location_Type']].drop_duplicates().set_index('Outlet_Identifier').to_dict()

    for outlet_id, info in outlet_info_map['Outlet_Size'].items():
        location_type = outlet_info_map['Outlet_Location_Type'][outlet_id]
        size = info
        fig_bar_grouped.add_annotation(
            x=outlet_id,  # Posição no eixo X (identificador da loja)
            y=-0.12,  # Coloca a anotação mais baixa
            text=f"Size: {size}<br>Location: {location_type}",  # Texto da anotação
            showarrow=False,
            font=dict(size=10, color="black"),
            align="center",
            bgcolor="rgba(255, 255, 255, 0.8)",  # Fundo transparente
            borderpad=4,
            borderwidth=1,
            bordercolor="gray",
            opacity=0.8,
            yref="y domain"  # Usando coordenadas relativas para colocar fora do gráfico
        )

    # Atualizando o layout do gráfico
    fig_bar_grouped.update_layout(
        xaxis=dict(
            title=dict(
                text='Loja',
                font=dict(size=14, color='black'),
                standoff=40  # Controla a distância do título ao eixo
            ),
        ),
        yaxis_title='Venda Total',
        legend_title='Tipo de produto',
        height=600,
        title_x=0.5,
        title_font=dict(color='black', size=20),
        plot_bgcolor='rgba(255, 255, 255, 0.8)',
        legend=dict(orientation='h', y=1.1),
        hovermode='x',
        hoverlabel=dict(bgcolor='white', font_size=12),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        font=dict(family='Arial, sans-serif', size=12, color='black'),
    )

    return fig_bar_grouped

# @title
def plot_visibility_boxplot(df):
    """
    Cria um gráfico de boxplot mostrando a distribuição da visibilidade por tipo de produto,
    com cores consistentes atribuídas a cada categoria.
    """
    # Garantir que todas as categorias têm cores atribuídas
    color_map = assign_colors(df, 'Item_Type')

    # Criar o Boxplot para distribuição de visibilidade por tipo de produto
    fig_box = px.box(
        df,
        x='Item_Type',
        y='Item_Visibility',
        color='Item_Type',
        title="Distribuição de Visibilidade por Tipo de Produto",
        labels={"Item_Visibility": "Visibilidade do Produto", "Item_Type": "Tipo de Produto"},
        color_discrete_map=color_map  # Aplicar cores consistentes da paleta
    )

    # Atualizar o layout do gráfico
    fig_box.update_layout(
        xaxis_title="Tipo de Produto",
        yaxis_title="Visibilidade do Produto",
        title_x=0.5,
        title_font=dict(color='black', size=20),
        plot_bgcolor='rgba(255, 255, 255, 0.8)',
        legend=dict(orientation='h', y=1.1),
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', font_size=12),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        font=dict(family='Arial, sans-serif', size=12, color='black'),
    )

    return fig_box


# @title
def plotly_visibility_vs_sales(df):
    """
    Plota a relação entre a visibilidade dos itens na loja e as vendas totais usando um gráfico de matriz de bolhas.
    As cores das bolhas representam o tipo de item ('Item_Type'), usando a função `assign_colors`.
    """

    # Calcular a porcentagem de vendas
    df['Sales Percentage'] = df['Item_Outlet_Sales'] / df['Item_Outlet_Sales'].sum() * 100

    # Garantir que todas as categorias de 'Item_Type' têm cores atribuídas
    color_map = assign_colors(df, 'Item_Type')

    # Criar o Bubble Matrix Plot
    fig_matrix_bubble = px.scatter(
        df,
        x='Item_Visibility',
        y='Item_Outlet_Sales',
        size='Sales Percentage',  # Tamanho da bolha representando a porcentagem de vendas
        color='Item_Type',  # Colorir com base em 'Item_Type'
        title="Relação entre Visibilidade e Vendas Totais",
        labels={"Item_Visibility": "Visibilidade do Produto", "Item_Outlet_Sales": "Vendas Totais"},
        color_discrete_map=color_map,  # Usando o mapa de cores gerado por `assign_colors`
        hover_data=['Item_Identifier', 'Outlet_Identifier'],
        template="plotly_white",  # Fundo branco para o gráfico
        facet_col='Outlet_Type',  # Cria uma matriz de gráficos separados por tipo de loja
        facet_col_wrap=2,  # Limita o número de colunas
        category_orders={"Outlet_Type": ['Grocery_Store', 'Supermarket_Type1', 'Supermarket_Type2', 'Supermarket_Type3']}  # Ordem dos gráficos
    )

    # Adicionar uma linha de tendência hipotética
    fig_matrix_bubble.add_trace(
        go.Scatter(
            x=df['Item_Visibility'],
            y=df['Item_Visibility'] * df['Item_Outlet_Sales'].mean(),  # Linha de tendência hipotética
            mode="lines",
            name="Linha de Tendência Hipotética",
            line=dict(color="red", dash="dot")
        )
    )

    # Ajustando a posição da legenda para cima
    fig_matrix_bubble.update_layout(
        legend=dict(
            orientation='h',  # Coloca a legenda na horizontal
            y=1.02,  # Posição da legenda acima do gráfico
            x=0.5,  # Centraliza a legenda
            xanchor='center',  # Centraliza a legenda horizontalmente
            yanchor='bottom'  # Coloca a legenda acima
        ),
        title=dict(
            text="Relação entre Visibilidade e Vendas Totais",
            font=dict(size=18),  # Tamanho da fonte do título
            x=0.5,  # Centraliza o título
            xanchor='center',  # Centraliza o título horizontalmente
            y=0.99,  # Garante que o título está na parte superior
        ),
        height=900  # Aumenta a altura do gráfico
    )

    return fig_matrix_bubble