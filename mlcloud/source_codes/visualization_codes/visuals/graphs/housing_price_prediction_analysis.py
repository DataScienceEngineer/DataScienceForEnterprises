import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from app_config import app

outdir='/storage/housing_price_prediction'

df1 = pd.read_csv(filepath_or_buffer=str(outdir+'/predout.csv'))
df1.rename(columns={'0': 'SalePrice_Predicted'}, inplace=True)
df2= pd.read_csv(filepath_or_buffer=str(outdir+'/test.csv'))
df=pd.merge(df1, df2, left_index=True,right_index=True)
years=df['YrSold'].unique()
years.sort()

layout = html.Div([
        html.H1(children='House Price Prediction Analysis (Actual vs Predicted)'),
        html.P(children='Filter data on the year the houses were sold'),
        dcc.Dropdown(
            id='year-sold-dropdown',
            options=[{'label': i, 'value': i} for i in years],
            value=None
        ),
        dcc.Graph(id='house-prediction-actual')
])

@app.callback(
    Output('house-prediction-actual', 'figure'),
    [Input('year-sold-dropdown', 'value')])
def update_graph(year_sold):
    if year_sold == None:
        dff=df
    else:
        dff = df[df['YrSold'] == year_sold]
    return {
            'data': [
                go.Scatter(
                    x=dff['SalePrice_Predicted'],
                    y=dff['SalePrice'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 8,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='hi'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Actual Price'},
                yaxis={'title': 'Predicted Price'},
                hovermode='closest'
            )
        }