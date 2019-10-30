from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class CompareMetricByAsset(Vis):
    def __init__(self, title:str,  metric:str, assets:[str]='all',):
        super().__init__(title=title)
        self.metric = metric
        self.assets = assets

    def implement_visualization(self, df):
        # if self.y_axis_columns == 'all':
        #     self.y_axis_columns = list(df.columns)
        fig = go.Figure()
        for asset in self.assets:
            fig.add_trace(go.Scatter(x=df.index, y=df[asset + '.' + self.metric],
                                mode='lines',
                                name=asset))
        self.fig = fig
