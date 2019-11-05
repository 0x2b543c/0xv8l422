from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChartAssetByMetrics(Vis):
    def __init__(self, title:str,  asset:str, metrics:[str]='all',):
        super().__init__(title=title)
        self.asset = asset
        self.metrics = metrics

    def implement_visualization(self, df):
        # if self.y_axis_columns == 'all':
        #     self.y_axis_columns = list(df.columns)
        fig = go.Figure()
        for metric in self.metrics:
            fig.add_trace(go.Scatter(x=df.index, y=df[self.asset + '.' + metric],
                                mode='lines',
                                name=metric))
        self.fig = fig
