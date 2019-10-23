from .VisualizationABC import Visualization as Vis
import pandas as pd
import plotly.graph_objects as go

class Table(Vis):
    def __init__(self, table_title:str, table_headers:[str], table_columns:[str]):
        self.title = table_title
        self.table_headers = table_headers
        self.table_columns = table_columns

    def create_visualization(self, df):
        fig = go.Figure(data=[go.Table(
            header={
                'values': self.table_headers,
                'fill_color': 'turquoise',
                'align': 'left'
            },
            cells={
                'values': [df[column] for column in self.table_columns],
                'fill_color': 'lavendar',
                'align': 'left'
            }
        ])
        return fig