from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChart(Vis):
    def __init__(self, title:str, y_axis_columns:[str]='all', x_axis_column:str='index'):
        super().__init__(title=title)
        self.y_axis_columns = y_axis_columns
        self.x_axis_column = x_axis_column

    def implement_visualization(self, df):
        if self.y_axis_columns == 'all':
            self.y_axis_columns = list(df.columns)
        fig = go.Figure()
        for column in self.y_axis_columns:
            fig.add_trace(go.Scatter(x=df.index if self.x_axis_column == 'index' else df[self.x_axis_column], y=df[column],
                                mode='lines',
                                name=column))
        self.fig = fig
