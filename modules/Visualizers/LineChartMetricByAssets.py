from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class LineChartMetricByAssets(Vis):
    def __init__(self, df, title:str,  metric:str, assets:[str]='all', section:str=None, order:int=None, y2_axis_columns:[str]=None, log_y_axis:bool=False):
        super().__init__(df=df, title=title, section=section, order=order)
        self.metric = metric
        self.assets = assets
        self.y2_axis_columns = y2_axis_columns
        self.log_y_axis = log_y_axis

    def implement(self):
        # if self.y_columns == 'all':
        #     self.y_columns = list(self.df.columns)
        fig = go.Figure()
        for asset in self.assets:
            fig.add_trace(go.Scatter(x=self.df.index, y=self.df[asset + '.' + self.metric],
                                mode='lines',
                                name=asset))

            if self.y2_axis_columns != None:
                for column in self.y2_axis_columns:
                    fig.add_trace(go.Scatter(x=self.df.index, y=self.df[column],
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
            if self.log_y_axis == True:
                fig.update_yaxes(type="log")
        self.fig = fig
