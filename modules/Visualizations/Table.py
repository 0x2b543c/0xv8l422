from .VisualizationABC import Visualization as Vis
import pandas as pd
import plotly.graph_objects as go

class Table(Vis):
    def __init__(self, title:str, table_headers:[str], table_columns:[str]):
        super().__init__(title=title)
        self.table_headers = table_headers
        self.table_columns = table_columns

    def implement_visualization(self, df):
        fig = go.Figure(data=[go.Table(
            header={
                'values': self.table_headers,
                'fill_color': 'skyblue',
                'align': 'left'
            },
            cells={
                'values': [df[column] for column in self.table_columns],
                'fill_color': 'snow',
                'align': 'left'
            }
        )])
        self.fig = fig