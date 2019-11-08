from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class MarketShareAssetsByMetric(Vis):
    def __init__(self, title:str, metric:str, assets:[str]):
        super().__init__(title=title)
        self.metric = metric
        self.assets = assets

    def implement_visualization(self, df):
        fig = go.Figure()
        for asset in self.assets:
            fig.add_trace(go.Scatter(x=df.index, y=df[asset + '.' + self.metric],
                                mode='lines',
                                name=asset,
                                stackgroup='one',
                                groupnorm='percent'))
        self.fig = fig
