from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChartMetricByAssets(Vis):
    def __init__(self, _id:int, df, title:str,  metric:str, assets:[str]='all', section:str=None, order:int=None):
        super().__init__(_id=_id, df=df, title=title, section=section, order=order)
        self.metric = metric
        self.assets = assets

    def implement(self):
        # if self.y_columns == 'all':
        #     self.y_columns = list(self.df.columns)
        fig = go.Figure()
        for asset in self.assets:
            fig.add_trace(go.Scatter(x=self.df.index, y=self.df[asset + '.' + self.metric],
                                mode='lines',
                                name=asset))
        self.fig = fig
