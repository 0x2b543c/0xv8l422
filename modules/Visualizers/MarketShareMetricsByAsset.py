from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class MarketShareMetricsByAsset(Vis):
    def __init__(self, df,  title:str, asset:str, metrics:[str]):
        super().__init__(df=df, title=title)
        self.asset = asset
        self.metrics = metrics

    def implement(self):
        fig = go.Figure()
        for metric in self.metrics:
            fig.add_trace(go.Scatter(x=self.df.index, y=self.df[self.asset + '.' + metric],
                                mode='lines',
                                name=metric,
                                stackgroup='one',
                                groupnorm='percent'))
        self.fig = fig
