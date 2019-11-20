from ..VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChartERCsAggregateMetric(Vis):
    def __init__(self, title:str, metric:str, add_eth:bool=True):
        super().__init__(title=title)
        self.metric = metric
        self.add_eth = add_eth

    def implement(self, df):
        fig = go.Figure()
        erc_metric_name = 'ERC-20' + '.' + self.metric
        fig.add_trace(go.Scatter(x=df.index, y=df[erc_metric_name],
                    mode='lines',
                    name=erc_metric_name))
        if self.add_eth == True:
            eth_metric_name =  'eth' + '.' + self.metric
            fig.add_trace(go.Scatter(x=df.index, y=df[eth_metric_name],
                    mode='lines',
                    name=eth_metric_name))
        self.fig = fig
