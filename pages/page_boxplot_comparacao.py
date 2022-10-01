### ------ IMPORTS ------ ###

# --- dash --- #
from dash import callback, dash_table, dcc, html, Input, Output, State
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# --- Third part --- #
from unidecode import unidecode
import pandas as pd

### ------ datasets ------ ####
from datasets import boxplot_data


### ------ Configs ------ ###
configuracoes_grafico = {
    'staticPlot': False,     # True, False
    'scrollZoom': True,      # True, False
    'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
    'showTips': True,       # True, False
    'displayModeBar': True,  # True, False, 'hover'
    'watermark': True,
    'modeBarButtonsToRemove': ['lasso2d'],
}


### ------ data for dropdown ------ ###
df_data_set_info = boxplot_data.df_data_set_info

dropdown_data_set_options = []

for i in range(df_data_set_info.shape[0]):
    dropdown_data_set_options.append({'label': df_data_set_info['data_set'][i], 'value': df_data_set_info['data_set'][i]})





### ------ LAYOUTS ------ ###
# --- MAIN LAYOUT --- #
layout = html.Div([
    # Titulo geral
    dbc.Row([
        dbc.Col(
            html.H2("Comparação entre métodos de cálculo dos quartis e seu impacto no Boxplot"),
            lg=10
        ),
    ], justify="center", style = {'textAlign': 'center', 'paddingTop': '30px', 'paddingBottom': '30px'},
    ),
    # Linha para separar tabela com dados e gráficos
    dbc.Row([
        dbc.Col([
            # Primeira linha com dropdown e info
            dbc.Row([
                # dataset dropdown
                dbc.Col(
                    dcc.Dropdown(
                        id="boxplot-comp-dropdown-dataset-picker", clearable=False,
                        value=dropdown_data_set_options[0]['value'],
                        options=dropdown_data_set_options
                    )
                ),
                # dataset tooltip
                dbc.Col(
                    html.I(className="fas fa-info-circle contact_icons", id='boxplot-comp-tootip-info-dataset'),
                    width='auto', align="center"
                ),
                dbc.Tooltip(
                    id="boxplot-comp-tootip-info-show",
                    target="boxplot-comp-tootip-info-dataset",
                    placement = 'right',
                ),

            ], ),
            # Seguna linha com a tabela com os dados
            dbc.Row([
                dbc.Col(
                    id='boxplot-comp-tabela-data-set', lg=6
                )
            ], className='title_spacing', justify='center'),
        ], lg=3),
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    html.H4("Comparativo de medidas de posição do Boxplot obtidas com diversos métodos."),
                    style={'textAlign': 'center'}
                ), className='title_spacing'
            ),
            dcc.Graph(id='boxplot-comp-bar-figure', config=configuracoes_grafico),
            dbc.Row(
                dbc.Col(
                    dcc.Markdown(children=[
                        '**Nota:** ',
                        '$q_{1}$: primeiro quartil, '
                        '$q_{3}$: terceiro quartil e '
                        '$IQR$: distância interquartílica'
                    ], mathjax=True, style={'textAlign': 'right', 'margin-right': '20px'})
                ), className='title_spacing'
            )
        ], lg=9),
    ], justify='center', className='title_spacing'),
    dbc.Row(
        dbc.Col(
            html.H3("Comparativo entre os Boxplots obtidos com os diversos métodos de estimação dos quartis."),
            style={"textAlign": 'center'}
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='boxplot-comp-boxplot-figure', config=configuracoes_grafico)
        ), className='title_spacing'
    ),




    # store dataset filtered
    dcc.Store(id='boxplot-comp-data-set'),
    dcc.Store(id='boxplot-comp-results'),


],)





### ------ CALLBACKS ------ ###

### ------ Callback to update boxplot data ------ ###
@callback(
    Output(component_id='boxplot-comp-tootip-info-show', component_property='children'),
    Output(component_id='boxplot-comp-data-set', component_property='data'),
    Output(component_id='boxplot-comp-results', component_property='data'),
    [
    Input(component_id='boxplot-comp-dropdown-dataset-picker', component_property='value'), # escolha do dataset
    ],
)
def filtering_dataset(dataset_key):
    # info data
    df_info = boxplot_data.df_data_set_info.copy()
    df_info = df_info[df_info['data_set'] == dataset_key]
    info = dcc.Markdown(df_info['infos'].values[0])


    # data-set
    df_data_set = boxplot_data.df_data_set.copy()
    df_data_set = df_data_set[df_data_set['data_set'] == dataset_key]
    df_data_set.reset_index(drop=True, inplace=True)
    df_data_set.drop(columns=['data_set'], inplace=True)



    # results
    df_results = boxplot_data.df_results .copy()
    df_results = df_results[df_results['data_set'] == dataset_key]
    df_results.reset_index(drop=True, inplace=True)



    return (info,
            df_data_set.to_json(date_format='iso', orient='split'),
            df_results.to_json(date_format='iso', orient='split'),
            )






# --- Callback to uptade the data-table --- #
@callback(
    Output(component_id='boxplot-comp-tabela-data-set', component_property='children'),
    [
    Input(component_id='boxplot-comp-data-set', component_property='data'),
    ]
)
def update_table_data(df_cleaned):
    # transforming data back to df
    df = pd.read_json(df_cleaned, orient='split').copy()
    df.rename(columns={df.columns[0]: 'Valores'}, inplace=True)

    # preparing columns
    columns = [
        dict(id=df.columns[0], name=df.columns[0], type='numeric')#, format=Format(precision=2, scheme=Scheme.fixed)),

    ]
    # criando a tabela
    table = dash_table.DataTable(
                columns = columns,
                data = df.to_dict('records'),
                style_data = {
                    'whiteSpace': 'normal',
                    'height': 'auto'
                    },
                style_table = {
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'maxHeight': '600px',
                    },
                style_cell = {
                    'font_size': 'clamp(1rem, 0.5vw, 0.5vh)',
                    'textAlign': 'center',
                    'height': 'auto',
                    # 'minWidth': '100px',
                    # 'width': '100px',
                    # 'maxWidth': '100px',
                    'whiteSpace': 'normal'
                },
                style_header = {
                    'fontWeight': 'bold', # deixando em negrito
                    }
              )


    # retornando a tabela
    return table






# --- Callback to uptade the boxplot --- #
@callback(
    Output(component_id='boxplot-comp-boxplot-figure', component_property='figure'),
    [
    Input(component_id='boxplot-comp-data-set', component_property='data'),
    Input(component_id='boxplot-comp-results', component_property='data'),
    ]
)
def update_boxplot_plot(df_cleaned, df_cleaned_2):
    # transforming data back to df
    df_data_set = pd.read_json(df_cleaned, orient='split').copy()
    df_results = pd.read_json(df_cleaned_2, orient='split').copy()

    fig = go.Figure()

    for i in range(df_results.shape[0]):
        fig.add_trace(go.Box(y=[df_data_set[df_data_set.columns[0]].to_numpy()],
                            name=df_results['method'][i], x=[i+1]))

        fig.update_traces(q1=[df_results['q1'][i]],
                          median=[df_results['median'][i]],
                          q3=[df_results['q3'][i]],
                          lowerfence=[df_results['lowerfence'][i]],
                          upperfence=[df_results['upperfence'][i]],
                          mean=[df_results['mean'][i]],
                          pointpos=0,
                          jitter=0,
                          boxpoints='outliers',
                          selector = dict(name=df_results['method'][i])
    )

    ### Atualizando o layout
    fig.update_layout(
            margin={"r":0,"l":0,"b":0, 't':30}, # removendo margens desnecessárias
            template='simple_white',
            hoverlabel = dict(
                bgcolor = "white",
                font_size = 16,
                font_family = "Rockwell"
            ),
            legend = dict(
                font_size = 16, font_family = "Rockwell",
            ),
    )

    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_xaxes(
        showline=True, linewidth=1, linecolor='black', mirror=True,
        ticktext=df_results['method'],
        tickvals=list(range(1,df_results.shape[0]+1)),
    )

    # retornando o grafico
    return fig






# --- Callback to uptade the barplot --- #
@callback(
    Output(component_id='boxplot-comp-bar-figure', component_property='figure'),
    [
    Input(component_id='boxplot-comp-data-set', component_property='data'),
    Input(component_id='boxplot-comp-results', component_property='data'),
    ]
)
def update_barplot_plot(df_cleaned, df_cleaned_2):
    # transforming data back to df
    df_data_set = pd.read_json(df_cleaned, orient='split').copy()
    df_results = pd.read_json(df_cleaned_2, orient='split').copy()


    df_results_bar_plot = pd.melt(df_results, id_vars=['method'], value_vars=['q1', 'q3', 'IQR'], var_name='Medida', value_name='valor')



    fig = px.bar(df_results_bar_plot, x=df_results_bar_plot.columns[0], y=df_results_bar_plot.columns[2],
                 color=df_results_bar_plot.columns[1], barmode='group',
                      )
    fig.update_layout(
            xaxis_title=None,
            margin={"r":0,"l":0,"b":0, 't':30}, # removendo margens desnecessárias
            template='simple_white',
            hoverlabel = dict(
                bgcolor = "white",
                font_size = 16,
                font_family = "Rockwell"
            ),
            legend = dict(
                font_size = 16, font_family = "Rockwell",
            ),
    )

    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    # retornando o grafico
    return fig























#
