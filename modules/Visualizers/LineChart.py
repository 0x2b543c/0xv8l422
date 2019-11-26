from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class LineChart(Vis):
    def __init__(self, df, title:str, y_columns:[str]='all', y2_axis_columns:[str]=None, x_axis_column:str='index'):
        super().__init__(df=df, title=title)
        self.y_columns = y_columns
        self.y2_axis_columns = y2_axis_columns
        self.x_axis_column = x_axis_column

    def implement(self):
        if self.y_columns == 'all':
            self.y_columns = list(self.df.columns)
        fig = go.Figure()
        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        for column in self.y_columns:
            fig.add_trace(go.Scatter(x=self.df.index if self.x_axis_column == 'index' else self.df[self.x_axis_column], y=self.df[column],
                                mode='lines',
                                name=column))
        if self.y2_axis_columns != None:
            for column in self.y2_axis_columns:
                fig.add_trace(go.Scatter(x=self.df.index if self.x_axis_column == 'index' else self.df[self.x_axis_column], y=self.df[column],
                                    mode='lines',
                                    name=column,
                                    yaxis='y2',
                                    marker= {
                                        'opacity': 0.5
                                    }))
            fig.update_layout(
                yaxis2=dict(
                    overlaying="y",
                    side="right"
                )
            )
        
        self.fig = fig
