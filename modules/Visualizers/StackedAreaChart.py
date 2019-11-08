from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class StackedAreaChart(Vis):
    def __init__(self, title:str, y_columns:[str]='all', x_column:str='index'):
        super().__init__(title=title)
        self.y_columns = y_columns
        self.y2_axis_columns = y2_axis_columns
        self.x_column = x_column

    def implement_visualization(self, df):
        if self.y_columns == 'all':
            self.y_columns = list(df.columns)
        fig = go.Figure()
        for column in self.y_columns:
            fig.add_trace(go.Scatter(x=df.index if self.x_column == 'index' else df[self.x_column], y=df[column],
                                mode='lines',
                                name=column,
                                stackgroup='one',
                                groupnorm='percent'))
        self.fig = fig
