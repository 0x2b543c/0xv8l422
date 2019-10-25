from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChart(Vis):
    def __init__(self, title:str, y_axis_columns:[str], x_axis_column:str='time'):
        super().__init__(title=title)
        self.y_axis_columns = y_axis_columns
        self.x_axis_column = x_axis_column

    def implement_visualization(self, df):
        fig = go.Figure()
        for column in self.y_axis_columns:
            fig.add_trace(go.Scatter(x=df[self.x_axis_column], y=df[column],
                                mode='lines',
                                name='lines'))
        self.fig = fig
