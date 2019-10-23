from .ChartABC import Chart as chart
import pandas as pd
import plotly.graph_objects as go

class Table(chart):
    def __init__(self, table_title:str, y_axis_columns:[str], x_axis_column:str='time'):
        self.table_title = None
        self.y_axis_columns = y_axis_columns
        self.x_axis_column = x_axis_column

    def create_table(self, df, table_headers:[str], table_columns:[str]):
        fig = go.Figure(data=[go.Table(
            header={
                'values': table_headers,
                'fill_color': 'turquoise',
                'align': 'left'
            },
            cells={
                'values': [df[column] for column in table_columns],
                'fill_color': 'lavendar',
                'align': 'left'
            }
        ])
        return fig