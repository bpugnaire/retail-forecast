from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from retail_forecast.predict import load_model

# df = preprocessing('data/train.csv')

model_dict = load_model()
# def generate_plot(department, bu):
#     prediction
#     fig1 = m.plot(forecast)
#     y = valid_dict[k]
#     y.plot(x='ds', y='y', ax=fig1.gca(), color='red')
#     return fig1

app = Dash()
list_store_dep = list(model_dict.keys())

#split the list_store_dep into one list for stores and one for departments
stores = []
departments = []
for store_dep in list_store_dep:
    store, dep = store_dep.split('-')
    if store not in stores:
        stores.append(store)
    if dep not in departments:
        departments.append(dep)
stores.sort()
departments.sort()

app.layout = [
    html.H1(children='Simple Turnover Timeseries Visualization', style={'textAlign':'center'}),
    dcc.Dropdown(
        id='dropdown-store',
        options=[{'label': "Magasin : " + store, 'value': store} for store in stores],
        value=stores[0]
    ),
    dcc.Dropdown(
        id='dropdown-department',
        options=[{'label': "BU : " +department, 'value': department} for department in departments],
        value=departments[0]
    ),
    
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-store', 'value'),
    Input('dropdown-department', 'value'),
)
def update_graph(store, department):
    m = model_dict[store+'-'+department]
    future = m.make_future_dataframe(periods=8,freq='W')
    forecast = m.predict(future)
    print(forecast.head())
    # use plotly express to plot the forecast
    fig = px.line(forecast[:-8], x='ds', y='yhat', title='Historical data for ' + store + ' - ' + department)
    #add the last 8 weeks of the training set to the plot in red
    fig.add_scatter(x=forecast[-8:]['ds'], y=forecast[-8:]['yhat'], mode='lines', name='Forecast', line=dict(color='red'))
    # confidence interval to the plot
    fig.add_scatter(x=forecast[-8:]['ds'], y=forecast[-8:]['yhat_upper'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', name='Upper Confidence Interval')
    fig.add_scatter(x=forecast[-8:]['ds'], y=forecast[-8:]['yhat_lower'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', name='Lower Confidence Interval')
    return fig
    
if __name__ == '__main__':
    app.run(debug=True, port=8050)
