from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChartAssetByMetrics(Vis):
    def __init__(self, df, title:str,  asset:str, metrics:[str]='all',section:str=None, order:int=None, filled_area:bool=False):
        super().__init__(df=df, title=title, section=section, order=order)
        self.df = df
        self.asset = asset
        self.metrics = metrics
        self.filled_area = filled_area

    def implement(self):
        # if self.y_columns == 'all':
        #     self.y_columns = list(df.columns)
        fig = go.Figure()
        for metric in self.metrics:
            fig.add_trace(go.Scatter(x=self.df.index, y=self.df[self.asset + '.' + metric],
                                mode='lines',
                                name=metric,
                                fill='tozeroy' if self.filled_area == True else 'none'))
        self.fig = fig
