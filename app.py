import numpy as np
import pandas as pd
import re
from urllib.parse import quote
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from helpers import (create_dropdown, read_uploaded_data, parse_contents,
                     make_predictions, text_intro, plotly_sales_by_category,
                     plotly_sales_over_outlet, plotly_visibility_vs_sales, plot_visibility_boxplot)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'styles.css'], suppress_callback_exceptions=True)

# Define um estilo específico para a guia "Sobre Este Web App"
sobre_style = {
    "background-color": "white",
    "margin": "20px auto",  # Centraliza no eixo horizontal
    "max-width": "1000px",  # Largura máxima alinhada às proporções da imagem
    'border-top': '1px solid #616161',
    'border': '1px solid #ccc',
    'border-radius': '5px',
    "padding": "20px"  # Espaçamento interno
}

# Logotipo da empresa
logo_empresa = html.Div([
    html.Img(
        src='https://raw.githubusercontent.com/wanderson42/BigMart-data/refs/heads/main/image_practice-problem-big-mart-sales-iii.png',
        style={
            'width': '100%',  # Proporção da largura
            'max-width': '1000px',  # Mantém a largura fixa alinhada ao estilo
            'height': 'auto',  # Ajusta automaticamente a altura
            'border-radius': '5px',
            'display': 'block',
            'margin': 'auto'
        }
    ),
], style={"margin": "0 0 10px", "overflow": "hidden"})

# Conteúdo para a página inicial "Sobre Este App"
def get_inicio_content():
    return html.Div([
        logo_empresa,
        html.H3("Sobre Este Web App", style={"padding-left": "20px", "padding-top": "10px"}),
        html.Hr(style={'border-top': '1px solid #616161'}),
        html.Div(
            text_intro(), 
            style={"padding-left": "20px", "padding-right": "20px"}  # Margens menores para texto
        ),
    ], style=sobre_style)  # Aplica o estilo personalizado


inicio_content = get_inicio_content()


# Define um estilo com fundo branco e margem lateral configurada para a guia Dashboard
pagina_style = {
    "background-color": "white",
    "margin": "20px auto",  # Margens ajustadas para centralizar no eixo horizontal
    "max-width": "1800px",  # Largura máxima da página
    'border': '1px solid #ccc',
    'border-radius': '5px',
    "padding": "20px"  # Adiciona espaço interno na página
}

# Conteúdo para a página "Dash Board De Previsões"
def get_previsoes_content():
    return html.Div([
        html.Div(style={'margin-top': '8px'}),  # Espaço adicional        
        html.H3("LinearRegressor - Previsão de Vendas"),
        # Adicione seus gráficos de previsões aqui
        # dcc.Graph(...)

        # Guias de opções e etiquetas
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Previsões Individuais', value='tab-1'),
            dcc.Tab(label='Previsões Multiplas', value='tab-2'),
            # dcc.Tab(label='Opção 3', value='tab-3'),
        ]),

        # Aqui, estamos criando um conteiner com o id="tabs-content", 
        # que será preenchido via callback com o conteúdo adequado de acordo 
        # com a guia (tab) selecionada.
        html.Div(id='tabs-content')

        # Adicionar mais conteúdo conforme necessário
    ], style={**pagina_style, "margin-top": "10px"})

previsoes_content = get_previsoes_content()



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Objeto para controlar a URL do aplicativo

    # Barra de navegação com melhor posicionamento
    dbc.Navbar(
        [
            # Logotipo à esquerda
            html.A(
                html.Img(
                    src="https://raw.githubusercontent.com/wanderson42/Portfolio-DS/main/datasets/Big_Mart_Sales/turing_logo.png",
                    height="50px",  # Ajusta o tamanho do logotipo
                    style={"margin-right": "20px"}  # Espaçamento entre o logotipo e as guias
                ),
                href="/",
                style={"display": "flex", "align-items": "center"}
            ),
            # Itens de navegação centralizados
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Sobre Este App", href="/", id="nav_inicio")),
                    dbc.NavItem(dbc.NavLink("DashBoard De Previsões", href="/predictions", id="nav_previsoes")),
                ],
                pills=True,
                style={"margin-left": "auto", "display": "flex", "align-items": "center"}  # Centraliza guias
            ),
        ],
        color="white",
        dark=False,
        style={
            "height": "70px",
            "padding": "10px 30px",  # Ajusta o espaçamento interno
            "box-shadow": "0px 2px 4px rgba(0, 0, 0, 0.1)",  # Sombra sutil
            "border-radius": "0 0 5px 5px",  # Apenas bordas inferiores arredondadas
            "display": "flex",  # Usa flexbox para alinhamento
            "align-items": "center"  # Alinha verticalmente os itens
        }
    ),

    # Conteúdo do NavItem
    html.Div(
        id="nav-content",
        style={
            "margin": "0 20px",
            "min-height": "calc(100vh - 90px)",  # Altura mínima da página sem a barra de navegação
            "padding": "20px",  # Adiciona espaço interno ao conteúdo
            "background-color": "#f5f5f5"  # Fundo claro
        }
    )
], style={"background-color": "#f5f5f5"})



'''
Aqui começa a parte dos callbacks
'''

# Callback para atualizar o conteúdo da página com base na URL
@app.callback(
    Output("nav-content", "children"),
    Output("nav_inicio", "className"),
    Output("nav_previsoes", "className"),
    Input("url", "pathname"),  # Monitora a URL atual
    prevent_initial_call=True
)
def update_nav_content(pathname):
    class_name_inicio = "nav-link"
    class_name_previsoes = "nav-link"
    if pathname == "/predictions":
        class_name_previsoes = "nav-link active"
        return previsoes_content, class_name_inicio, class_name_previsoes
    else:
        class_name_inicio = "nav-link active"
        return inicio_content, class_name_inicio, class_name_previsoes  # Página "Sobre Este App" como padrão


# Callback exclusivo para filtrar as opções do Item_Identifier conforme o usuário digita:
@app.callback(
    Output('dropdown-Item_Identifier', 'options'),
    Input('dropdown-Item_Identifier', 'search_value'),
    prevent_initial_call=True
)
def update_item_identifier_options_from_csv(search_value):
    """
    Filtra as opções de Item_Identifier dinamicamente usando um arquivo CSV.
    """
    if not search_value:
        raise dash.exceptions.PreventUpdate

    # Carregar o CSV com os identificadores
    csv_path = './item_identifiers.csv'  # Caminho para o arquivo na raiz do projeto
    df = pd.read_csv(csv_path)

    # Filtrar os identificadores que contêm o valor buscado
    filtered_options = df[df['Item_Identifier'].str.contains(search_value, case=False, na=False)]

    # Retornar as opções formatadas para o Dropdown
    return [{'label': identifier, 'value': identifier} for identifier in filtered_options['Item_Identifier']]


# Callback principal do dashboard
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    '''
    A função render_content é o callback que responde à interação
    do usuário com as guias (tabs).
     
    Este callback é ativado sempre que o valor de uma guia (tabs) muda,
    ou seja, verifica qual guia o usuario seleciona e retorna o conteúdo
    correspondente a essa guia.
    '''
    
    if tab == 'tab-1':
        return html.Div([
            html.Div(style={'margin-top': '8px'}),  # Espaço adicional
            html.H4('Selecione os atributos para realizar uma previsão:'),
            html.Div([
                html.Br(),
                # Adicione os Dropdowns para as features discretas
                html.Div([
                    create_dropdown("Outlet_Identifier", searchable=False),
                ], style={"margin-right": "20px", "margin-bottom": "20px", "display": "inline-block", "width": "200px", "vertical-align": "top"}),

                # Dropdown com busca para Item Identifier
                html.Div(
                    create_dropdown("Item_Identifier", searchable=True),
                    style={"margin-right": "20px", "margin-bottom": "20px", "display": "inline-block", "width": "300px"}
                ),

                html.Br(), # Quebra de linha após o terceiro dropdown

                html.Div([
                    create_dropdown("Item_Type"),
                ], style={"margin-right": "20px", "margin-bottom": "20px", "display": "inline-block", "width": "200px", "vertical-align": "top"}),


                html.Div([
                    create_dropdown("Item_Fat_Content"),
                ], style={"margin-right": "20px", "margin-bottom": "20px", "display": "inline-block", "width": "200px", "vertical-align": "top"}),

                html.Br(),  # Quebra de linha após o quarto dropdown 

                html.Div([
                    html.H6("Item_Visibility (0 – 5):"),
                    dcc.Input(id='input-Item_Visibility', type='number', value=0, min=0, max=0.5, step=0.01, style={ "width": "180px"}),
                ], style={"margin-right": "20px", "margin-bottom": "20px","display": "inline-block", "width": "200px", "vertical-a lign": "top"}),

                html.Div([
                    html.H6("Item_MRP (0 – 1000):"),
                    dcc.Input(id='input-Item_MRP', type='number', value=0, min=0, max=1000, step=0.01, style={ "width": "180px"}),
                ], style={"margin-right": "20px", "margin-bottom": "20px", "display": "inline-block",  "width": "200px", "vertical-align": "top"}),

            ]),

            # Botão de Fazer Previsão
            html.Button('Fazer Previsão',id='submit-button', n_clicks=0, style={
                'margin-top': '0px', 'background-color': '#f1863d',
                'text-align': 'center', 'padding': '5px',
                'border-radius': '5px', 'color': 'black',
                'text-decoration': 'none', 'display': 'block'  # Criar um espaço abaixo do botão
                }),
            # Exibição da previsão
            html.Div(id='individual-prediction')
        ])
    
    #Condicional para acessar a opção de multiplas previsões
    elif tab == 'tab-2':
        return html.Div([
            html.Div(style={'margin-top': '8px'}),  # Espaço adicional
            html.H4('Certifique-se que os dados estejam adequadamente padronizados com base'),
            html.H4('nos atributos informativos:'),
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Arraste e solte ou ',
                        html.A('selecione um arquivo .csv')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px 0'
                    },
                    # Permite upload de apenas um arquivo
                    multiple=False
                ),
                html.Div(id='output-data-upload'),
            ]),
            # Adicione seu conteúdo da opção 2 aqui
            html.Div(style={'margin-top': '8px'}),  # Espaço adicional
            #html.Button('Fazer Previsões', id='submit-button', n_clicks=0, style={'background-color': '#f1863d',
            #                                                                      'position': 'relative', 'left':'750px'}),

            html.Div(id='multiple-predictions')

        ])


# Callback para receber os dados de previsão individual
@app.callback(
    Output('individual-prediction', 'children'),
    Input('submit-button', 'n_clicks'),
    [
    State('dropdown-Outlet_Identifier', 'value'),
    State('dropdown-Item_Identifier', 'value'),    
    State('dropdown-Item_Type', 'value'),
    State('dropdown-Item_Fat_Content', 'value'),  
    State('input-Item_Visibility', 'value'),
    State('input-Item_MRP', 'value')
    ],
    prevent_initial_call=True
)
def update_individual_prediction(n_clicks, outlet_identifier, item_identifier, 
                                 item_type, item_fat_content, item_visibility, item_mrp):
    if n_clicks == 0:
        raise PreventUpdate

    if not all([outlet_identifier, item_identifier, item_type, item_fat_content, item_visibility, item_mrp]):
        return html.H5("Por favor, preencha todos os campos antes de realizar a previsão.", style={'color': 'red'})


    user_input = {
        'Outlet_Identifier': outlet_identifier,
        'Item_Identifier': item_identifier,
        'Item_Type': item_type,
        'Item_Fat_Content': item_fat_content,
        'Item_Visibility': item_visibility,
        'Item_MRP': item_mrp
    }
   
    # Fazer a previsão
    try:
        prediction = make_predictions(user_input)  # Função customizada para realizar as previsões
        prediction_rounded = np.round(prediction, 2)  # Arredondar resultado
        result_text = f"**Resultado:**  \nItem_Outlet_Sales = R$ {prediction_rounded[0]:,.2f}"
    except Exception as e:
        result_text = f"Erro ao realizar previsão: {str(e)}"

    # Retornar resultado formatado
    return html.H5(dcc.Markdown(result_text), style={'margin-top': '10px'})


# Visualização de múltiplas previsões
html.Div([
    dcc.Graph(id='multiple-predictions'),  # Use dcc.Graph para mostrar um gráfico
    html.A('Baixar Previsões', id='download-predictions', 
         download="predictions.csv", href="", target="_blank", 
         style={     
        'display': 'none'  # Oculta o link na página
    })

])

# ...

# callback para chamar a função parse_contents quando um arquivo .csv for carregado:
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        raise PreventUpdate
    return parse_contents(contents)


# Callback para múltiplas previsões
@app.callback(
    Output('multiple-predictions', 'children'),
    Input('submit-button', 'n_clicks'),
    State('upload-data', 'contents')  # Adicionando o conteúdo do arquivo
)
def update_multiple_predictions(n_clicks, contents):

    if n_clicks == 0 or contents is None:
        raise PreventUpdate

    # Dados obtidos a partir do upload do usuario
    user_inputs = read_uploaded_data(contents)

    # Fazendo previsões com base nas entradas do usuário
    predictions = make_predictions(user_inputs)

    predictions = np.round(predictions, 2)

    # Criar uma Panda.Series para as previsões
    item_outlet_sales = pd.Series(predictions, name='Item_Outlet_Sales')

    # Concatenar a série de previsões com o dataframe user_inputs
    result_df = pd.concat([user_inputs.reset_index(drop=True), item_outlet_sales.reset_index(drop=True)], axis=1)


    # Criar o DataFrame final com apenas as colunas necessárias
    df_preds = pd.concat([
        user_inputs[['Outlet_Identifier', 'Item_Identifier']].reset_index(drop=True),
        item_outlet_sales.reset_index(drop=True)
    ], axis=1)
    
    # Criando a tabela de resultados das previsões
    table = dash_table.DataTable(
        data=df_preds.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df_preds.columns],
        style_table={'height': '350px', 'overflowY': 'auto', 'position': 'relative'},
        id='results-table'  # Adicionando um ID à tabela para referência posterior
    )

    # Gráfico Distribuição de Vendas por Categoria
    plotly_1 = plotly_sales_by_category(result_df)

    # Gerando link para download do CSV
    csv_string = df_preds.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + quote(csv_string)


    # Ajustando o botão de download
    download_href = csv_string
    download_button = html.A('Baixar Previsões', id='download-predictions', download="predictions.csv",
                             href=download_href, target="_blank",
                             style={'background-color': '#2E9203', 'margin-top': '-60px',
                                    'display': 'block', 'width': '130px', 'text-align': 'center',
                                    'padding': '5px', 'border-radius': '5px', 'color': 'black',
                                    'text-decoration': 'none','margin-bottom': '10px'})

    # Gráfico Distribuição de Vendas por Categoria em cada loja
    plotly_2 = plotly_sales_over_outlet(result_df)

    # Gráfico de distribuição da visibilidade dos items
    plotly_3 = plot_visibility_boxplot(result_df)

    # Gráfico de visibilidade vs vendas
    plotly_4 = plotly_visibility_vs_sales(result_df)


    # Layout para empilhar os gráficos
    return html.Div([
        html.H5('Resultado das Previsões:'),
        dbc.Row([
            dbc.Col(html.Div([table]), width=4),
            dbc.Col(html.Div([dcc.Graph(figure=plotly_1, id='sales-graph')]), width=8)
        ]),
        download_button,  # Botão de download
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(figure=plotly_2, id='second-sales-graph')]), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(figure=plotly_3, id='third-sales-graph')]), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(figure=plotly_4, id='fourth-sales-graph')]), width=12)
        ]),                  
    ], style={'width': '100%'})


if __name__ == '__main__':
    app.run_server(debug=True)
