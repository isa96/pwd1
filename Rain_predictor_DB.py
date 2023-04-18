import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output,State
import pickle

loadmodel = pickle.load(open('Legendary_predictor.sav','rb'))
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dfPokemon = pd.read_csv('Pokemon.csv')

pokemon = dfPokemon[['Total','Attack','Defense','Generation','Legendary']]

app.layout = html.Div(children = [
        html.H1('Ini Dashboard'),
        html.P('Created by: Cornelis'),
        dcc.Tabs(value='tabs',id='tabs-1',children = [
            dcc.Tab(label='Bar-Chart',value='tabsatu',children = [
                html.Div(className='row',children=[
                    html.Div([
                        html.H5('X1'),
                        dcc.Dropdown(id='x1',
                            options = [{'label':i, 'value':i} for i in dfPokemon.select_dtypes('number').columns],
                            value = 'Attack'
                        )
                    ],
                ),
                    html.Div([html.H5('X2'),
                        dcc.Dropdown(id='x2',
                            options = [{'label':i, 'value':i} for i in dfPokemon.select_dtypes('number').columns],
                            value = 'Attack'
                        )
                    ],className='col-3')
                ]),
                
                html.Div([
                    dcc.Graph(
                    id = 'contoh-graph-bar',
                    figure={
                    'data':[
                        {'x': dfPokemon['Generation'],'y':dfPokemon['Attack'],'type':'bar','name':'Attack'},
                        {'x': dfPokemon['Generation'],'y':dfPokemon['Speed'],'type':'bar','name':'Speed'}
                    ],
                        'layout':{'title':'Graph Bar'}
                    }
                        )])
            ],className='col-3'),
            dcc.Tab(label='Pie-Chart',value='tabtwo',children = [
                html.Div([ 
                    html.H5('X1'),
                        dcc.Dropdown(id='xsatu',
                            options = [{'label':i, 'value':i} for i in dfPokemon.select_dtypes('number').columns],
                            value = 'Attack'
                        )]),
                html.Div([
                    dcc.Graph(
                    id = 'contoh-graph-pie',
                    figure = 
                    {
                        'data': [
                            go.Pie(labels=['Generation {}'.format(i) for i in list(dfPokemon['Generation'].unique())],
                            values = [dfPokemon.groupby('Generation').mean()['Attack'][i] for i in list(dfPokemon['Generation'].unique())],
                            sort = False)
                        ],
                            'layout' : {'title':'Mean Pie Chart'}
                    }
                    )
                ],className ='col-12')
            ]),
            dcc.Tab(label='Scatter-Chart',value='tabtiga',children=
                dcc.Graph(
                    id = 'graph-scatter',
                    figure = {
                        'data': [
                            go.Scatter(
                                x = dfPokemon[dfPokemon['Generation']==i]['Attack'],
                                y = dfPokemon[dfPokemon['Generation']==i]['Speed'],
                                text = dfPokemon[dfPokemon['Generation']==i]['Name'],
                                mode = 'markers',
                                name = 'Generation {}'.format(i)
                            ) for i in dfPokemon['Generation'].unique()
                        ],
                        'layout' : 
                            go.Layout(
                                xaxis = {'title':'Attack Pokemon'},
                                yaxis = {'title': 'Speed Pokemon'},
                                hovermode = 'closest'
                            )
                    }   
                )
            ),
            dcc.Tab(label='Table',value='tabempat',children=[
                html.H1('DATAFRAME POKEMON',style ={'textAlign':'center'}),
                html.Div(children=[
                    html.P('Generation:'),
                    dcc.Dropdown(
                        id='gen',
                            options = [{'label':i, 'value':i} for i in dfPokemon['Generation'].unique()],
                            value = 1,className = 'col-3'),
                    html.P('Max Rows:'),
                    dcc.Input(id='num',type ='number',value = 5),
                ]),
                html.Div(id='abc',children=[
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in dfPokemon.columns],
                        data=dfPokemon.to_dict('records'),
                        page_action = 'native',
                        page_current = 0,
                        page_size = 10, 
                    )
                ]),
                html.Div(
                    html.Button('Search',id = 'tablesearch')
                )]
            ),
            dcc.Tab(label='Legendary Pokemon Prediction',value='tablima',children=[
                html.Div([
                    html.Div([
                        html.P('Total'),
                        dcc.Input(id='num1',type ='number',value = 0)
                    ],className = 'col-3'),
                    html.Div([
                        html.P('Attack'),
                        dcc.Input(id='num2',type='number',value=0)
                    ],className ='col-3'),
                    html.Div([
                         html.P('Defense'),
                        dcc.Input(id='num3',type='number',value=0)
                    ],className ='col-3'),
                    html.Div([
                        html.P('Generation'),
                        dcc.Input(id='num4',type='number',value =0)
                    ],className ='col-3')
                ],className = 'row'),
                html.Div([
                    html.Button('Search',id = 'Predict')
                ]),
                html.H1(id = 'result',children = '')
        ])
                # html.H1('Your Pokemon is {} with Probability {}%'.format(),id= 'result'),
                # html.Div(
                # dash_table.DataTable(
                #     id='table',
                #     columns=[{"name": i, "id": i} for i in dfPokemon.columns],
                #     data=dfPokemon.to_dict('records'),
                #     page_action = 'native',
                #     page_current = 0,
                #     page_size = 10,
                # ))], 
                # className = 'col-3')
                # dcc.Tab(label='Legendary Pokemon Prediction',value='tablima',children=
                # dcc.Graph(
                #     id = 'graph-scatter',
                #     figure = {
                #         'data': [
                #             go.Scatter(
                #                 x = dfPokemon[dfPokemon['Generation']==i]['Attack'],
                #                 y = dfPokemon[dfPokemon['Generation']==i]['Speed'],
                #                 text = dfPokemon[dfPokemon['Generation']==i]['Name'],
                #                 mode = 'markers',
                #                 name = 'Generation {}'.format(i)
                #             ) for i in dfPokemon['Generation'].unique()
                #         ],
                #         'layout' : 
                #             go.Layout(
                #                 xaxis = {'title':'Attack Pokemon'},
                #                 yaxis = {'title': 'Speed Pokemon'},
                #                 hovermode = 'closest'
                #             )
                #     }   
                # ), 
                # className = 'col-3')    

            ],
            content_style = {
                'fontFamily':'Arial',
                'borderBottom':'100px solid #d6d6d6',
                'borderLeft':'100px solid #d6d6d6',
                'borderRight':'100px solid #d6d6d6',
                'padding':'44px'
                }
            
            )
],style = {
    'maxwidth':'1200px',
    'margin':'0 auto'
}
)

# @app.callback(
#     Output(component_id='contoh-graph-bar', component_property='figure'),
#     [Input(component_id = 'x1', component_property='value'),
#     Input(component_id = 'x2',component_property='value')]
# )
# def create_graph(x1,x2):
#     figure = {
#         'data':[
#             {'x':dfPokemon['Generation'],'y':dfPokemon[x1],'type':'bar','name':x1},
#             {'x':dfPokemon['Generation'],'y':dfPokemon[x2],'type':'bar','name':x2}
#         ],
#         'layout':{'title':'Bar Chart'}
#     }
#     return figure 
@app.callback(
    Output(component_id='abc',component_property='children'),
    [Input(component_id='tablesearch',component_property ='n_clicks')],
    [State(component_id = 'gen',component_property='value'),
    State(component_id= 'num',component_property= 'value')]
)
def create_graph(n_clicks,gen,num):

    table=dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfPokemon.columns],
        data=dfPokemon[dfPokemon['Generation']==gen].to_dict('records'),
        page_action = 'native',
        page_current = 0,
        page_size = num, 
    )

    return table

@app.callback(
    Output(component_id='result',component_property = 'children'),
    [Input(component_id='Predict',component_property ='n_clicks')],
    [State(component_id='num1',component_property='value'),
    State(component_id='num2',component_property='value'),
    State(component_id='num3',component_property='value'),
    State(component_id='num4',component_property='value')]
)
def prediction(n_clicks,num1,num2,num3,num4):
    
    x = loadmodel.predict_proba(np.array([[num1,num2,num3,num4]]))
    y=[]
    legend_calc=[]
    for i in range(2):
        y.append(round(x[0][i]*100,ndigits =2))
        res = max(y)
    if x[0][0]>x[0][1]:
        legend_calc.append('Non-Legendary')
    else:
        legend_calc.append('Legendary')

    out = ['Your Pokemon is {} with Probability {}%'.format(legend_calc[0],res)]
    return out
    # html.Div(
    #             dash_table.DataTable(
    #                 id='table',
    #                 columns=[{"name": i, "id": i} for i in dfPokemon.columns],
    #                 data=dfPokemon.to_dict('records'),
    #                 page_action = 'native',
    #                 page_current = 0,
    #                 page_size = x2,
    #             )
# )

if __name__ == '__main__':
    app.run_server(debug=True)
