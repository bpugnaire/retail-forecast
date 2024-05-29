from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from retail_forecast.predict import predict

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

prediction = predict()

# def generate_plot(department, bu):
#     prediction
#     fig1 = m.plot(forecast)
#     y = valid_dict[k]
#     y.plot(x='ds', y='y', ax=fig1.gca(), color='red')
#     return fig1

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
