from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class LineChart(Vis):
    def __init__(self, df, title:str, y_columns:[str]='all', y2_axis_columns:[str]=None, x_axis_column:str='index', section:str=None, growth=None, filled_area:bool=False, stacked:bool=False, seven_day_rolling_average=False):
        super().__init__(df=df, title=title, section=section, growth=growth, seven_day_rolling_average=seven_day_rolling_average)
        self.y_columns = y_columns
        self.y2_axis_columns = y2_axis_columns
        self.x_axis_column = x_axis_column
        self.filled_area = filled_area
        self.stacked = stacked

    def implement(self):
        # plotly_colors = [
        #     '#1f77b4',  # muted blue
        #     '#ff7f0e',  # safety orange
        #     # '#2ca02c',  # cooked asparagus green
        #     '#d62728',  # brick red
        #     '#9467bd',  # muted purple
        #     '#8c564b',  # chestnut brown
        #     '#e377c2',  # raspberry yogurt pink
        #     '#7f7f7f',  # middle gray
        #     '#bcbd22',  # curry yellow-green
        #     '#17becf'   # blue-teal
        # ]

        plotly_colors = [
            'aquamarine',
            'yellowgreen',
            'lightgray',
            'orangered',
            'coral',
            'purple',
            'peachpuff'

        ]

        # plotly_colors = ['aliceblue',  'aqua', 'aquamarine', 'darkturquoise']
        if self.y_columns == 'all':
            self.y_columns = list(self.df.columns)
        fig = go.Figure()
        # fig = make_subplots(specs=[[{"secondary_y": True}]])
        color_counter = 0
        for column in self.y_columns:
            fig.add_trace(go.Scatter(x=self.df.index if self.x_axis_column == 'index' else self.df[self.x_axis_column], y=self.df[column],
                                mode='lines',
                                name=column,
                                marker = {
                                    'color': '#0381E0' if len(self.y_columns) < 2 else None
                                },
                                fill='tonexty' if self.filled_area == True else 'none',
                                stackgroup='one' if self.stacked == True else None
                                ))
            color_counter += 1                                
        if self.y2_axis_columns != None:
            for column in self.y2_axis_columns:
                fig.add_trace(go.Scatter(x=self.df.index if self.x_axis_column == 'index' else self.df[self.x_axis_column], y=self.df[column],
                                    mode='lines',
                                    name=column,
                                    yaxis='y2',
                                    line = {
                                        'width': 2
                                    },
                                    marker= {
                                        'opacity': 0.25,
                                        'color': 'black',
                                        # 'symbol': 'circle-dot',
                                        'size': 1

                                    }))
            fig.update_layout(
                yaxis2=dict(
                    overlaying="y",
                    side="right"
                )
            )
        
        self.fig = fig
