from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go
import math

class Table(Vis):
    def __init__(self, df, title:str, table_headers:[str], table_columns:[str], column_order:[int]=None):
        super().__init__(df=df, title=title)
        self.table_headers = table_headers
        self.table_columns = table_columns
        self.column_order = column_order
    
    def create_row_colors(self):
        number_of_rows = self.df.shape[0]
        number_of_columns = self.df.shape[1]
        rowOddColor = 'rgb(242, 242, 242)'
        rowEvenColor = 'white'
        row_colors = []
        for i in range(number_of_rows):
            if i % 2 == 0:
                row_colors.append(rowEvenColor)
            else:
                row_colors.append(rowOddColor)
        return [row_colors * number_of_columns]


    def implement(self):
        header_color = 'lightgrey'

        fig = go.Figure(data=[go.Table(
            header={
                'values': self.table_headers,
                'fill_color': header_color,
                'align': 'left'
            },
            cells={
                'values': [self.df[column] for column in self.table_columns],
                'fill_color': 'snow',
                'fill_color': self.create_row_colors(),
                'align': 'left'
            },
            columnorder=self.column_order
        )])
        self.fig = fig
