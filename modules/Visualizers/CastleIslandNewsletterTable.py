from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go

class CastleIslandNewsletterTable(Vis):
    def __init__(self, df, title:str, assets:[str], metrics:[str], table_headers:[str], table_columns:[str]):
        super().__init__(title=title)
        self.table_headers = table_headers
        self.table_columns = table_columns

    # Asset PriceUSD PriceUSD.1dGrowth PriceUSD.7dGrowth MarketCap RealizedCap

    
    def implement(self, df):
        fig = go.Figure(data=[go.Table(
            header={
                'values': self.table_headers,
                'fill_color': 'skyblue',
                'align': 'left'
            },
            cells={
                'values': [df[[column for column in df.columns if column.split('.')[0] == asset]] for asset in assets]
                'align': 'left'
            }
        )])
        self.fig = fig