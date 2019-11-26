import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

class DashLineChartAssetByMetrics():
    def __init__(self, title:str,  asset:str, metrics:[str]='all',):
        self.title= title
        self.asset = asset
        self.metrics = metrics
        self.fig = None

    def implement(self, df):
        fig = {
            'data': []
        }
        for metric in self.metrics:
            metric_data = {
                'x': df.index,
                'y': df[f'{self.asset}.{metric}'],
                'mode': 'lines',
                'name': metric
            }
            fig['data'].append(metric_data)
        
        self.fig = fig
        return self

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

test_columns = ['btc.TxCnt', 'btc.TxTfrCnt', 'eth.TxCnt', 'eth.TxTfrCnt']
test_data = [
    [100, 110, 55, 13],
    [120, 130, 65, 33],
    [300, 140, 55, 13],
    [200, 120, 65, 33],
    [100, 110, 55, 13],
]
test_index = [
    '2019-01-01',
    '2019-01-02',
    '2019-01-03',
    '2019-01-04',
    '2019-01-05'
]

test_df = pd.DataFrame(data=test_data, columns=test_columns)
test_df.index = test_index

chart = DashLineChartAssetByMetrics(title='test', asset='eth', metrics=['TxCnt', 'TxTfrCnt']).implement(test_df)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure= chart.fig
    )
])


app.run_server(debug=True)