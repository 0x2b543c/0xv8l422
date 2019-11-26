from ..VisualizerABC import Visualizer as Vis
import pandas as pd

class DashLineChartAssetByMetrics(Vis):
    def __init__(self, title:str,  asset:str, metrics:[str]='all',):
        super().__init__(title=title)
        self.asset = asset
        self.metrics = metrics

    def implement(self, df):
        # if self.y_columns == 'all':
        #     self.y_columns = list(df.columns)
        fig = {
            data: []
        }
        for metric in self.metrics:
            metric_data = {
                'x': df.index,
                'y': df[f'{self.asset}.{metric}']
                'mode': 'lines',
                'name': metric
            }
            fig['data'].add(metric_data)
        
        self.fig = fig
