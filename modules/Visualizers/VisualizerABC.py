from abc import ABC, abstractmethod
from ..Transformers.PercentGrowth import PercentGrowth
from ..Transformers.RollingAverage import RollingAverage
from ..Transformers.DatePicker import DatePicker
from ..Transformers.DateWindow import DateWindow
from ..Transformers.SliceDFStart import SliceDFStart
from pathlib import Path
import pdb
import pandas as pd

class Visualizer(ABC):
    def __init__(
        self, 
        df, 
        title:str, 
        x_column:str='index', 
        y_columns:[str]=None, 
        assets:[str]=None, 
        metrics:[str]=None, 
        custom_formatting:str=None, 
        growth:str=None, 
        seven_day_rolling_average:str=None, 
        start:str=None, 
        end:str=None, 
        date_window:str=None, 
        annotations:bool=True, 
        showlegend:bool=True,
        slice_to_df_start:bool=False,
        y_log:bool=False,
        y2_log:bool=False
        ):

        self.df = df
        self.title = title
        self.custom_formatting = custom_formatting
        self.fig = None
        # Display Options
        # TODO: Add these as params
        self.growth = growth
        self.seven_day_rolling_average = seven_day_rolling_average
        self.start = start
        self.end = end
        self.date_window = date_window
        self.assets = assets
        self.metrics = metrics
        self.x_column = x_column
        self.y_columns = y_columns if y_columns else self.convert_assets_and_metrics_to_columns(assets=self.assets, metrics=self.metrics)
        self.annotations = annotations
        self.showlegend = showlegend
        self.slice_to_df_start = slice_to_df_start
        self.y_log = y_log
        self.y2_log = y2_log
        self.metric_mappings = {
            'Asset': 'Asset',
            'CapRealUSD' : 'Realized Cap',
            'CapMrktCurUSD': 'Market Cap',
            'CapMVRVCur': 'Market Value to Realized Value (MVRV) ',
            'VtyDayRet30d': 'Volatility, 30d',
            'PriceUSD': 'Price, USD',
            'AdrActCnt': 'Active Addresses',
            'AdrBalUSD10Cnt': 'Addresses with Balance >= $10',
            'AdrBalUSD1MCnt': 'Addresses with Balance >= $1M',
            'SplyAct30d': 'Active Supply, 30d',
            'SplyAct30dPercent' : 'Active Supply Percentage, 30d',
            'BlkSizeByte': 'Block Size, Bytes',
            'TxCnt': 'Transaction Count',
            'TxTfrCnt': 'Transfer Count',
            'TxTfrValAdjUSD': 'Adjusted Transfer Value',
            'IssContPctAnn': 'Issuance, Annualized',
            'FeeMedUSD': 'Median Transaction Fee',
            'HashRate': 'Hash Rate',
            'DiffMean': 'Difficulty, Mean',
            'FeeTotUSD': 'Fees, USD',
            'FeeRevPct': 'Fee to Revenue Percentage',
            'RevUSD': 'Miner Revenue, USD'          
        }



    @abstractmethod
    def implement(self, df):
        pass

    def convert_assets_and_metrics_to_columns(self, assets:[str], metrics:[str]):
        df_columns = list(self.df.columns)
        columns = []
        for asset in assets:
            for metric in metrics:
                new_column = f'{asset}.{metric}'
                columns.append(new_column)
        return columns

    def map_column_names_to_human_readable(self, columns):
        return list(map(lambda column_name: self.convert_column_name_to_human_readable(column_name), list(columns)))

    def convert_column_name_to_human_readable(self, column_name):
        metric_mappings = {
            'Asset': 'Asset',
            'CapRealUSD' : 'Realized Cap',
            'CapMrktCurUSD': 'Market Cap',
            'CapMVRVCur': 'Market Value to Realized Value (MVRV) ',
            'VtyDayRet30d': 'Volatility, 30d',
            'PriceUSD': 'Price, USD',
            'AdrActCnt': 'Active Addresses',
            'AdrBalUSD10Cnt': 'Addresses with Balance >= $10',
            'AdrBalUSD1MCnt': 'Addresses with Balance >= $1M',
            'SplyAct30d': 'Active Supply, 30d',
            'SplyAct30dPercent' : 'Active Supply Percentage, 30d',
            'BlkSizeByte': 'Block Size, Bytes',
            'TxCnt': 'Transaction Count',
            'TxTfrCnt': 'Transfer Count',
            'TxTfrValAdjUSD': 'Adjusted Transfer Value',
            'IssContPctAnn': 'Issuance, Annualized',
            'FeeMedUSD': 'Median Transaction Fee',
            'HashRate': 'Hash Rate',
            'DiffMean': 'Difficulty, Mean',
            'FeeTotUSD': 'Fees, USD',
            'FeeRevPct': 'Fee to Revenue Percentage',
            'RevUSD': 'Miner Revenue, USD'          
        }
        asset_and_metric = column_name.split('.')
        asset = asset_and_metric[0] if len(asset_and_metric) > 1 else None
        metric = asset_and_metric[1] if len(asset_and_metric) > 1 else None
        if metric in list(metric_mappings.keys()):
            column_name = f'{asset} {metric_mappings[metric]}'
        return column_name

    def show(self):
        # TODO: Put in check for visual type (e.g. Plotly, Matplot, etc.)
        return self.fig.show()

    def export(self, title:str, repo:str):
        file_path = str(Path(__file__).parent.parent.parent) + '/pngs/{}/{}.png'.format(repo, title)
        # file_path = "/pngs/{}.png".format(visual.title)
        self.fig.write_image(file_path)

    def update_fig_layout(self):
        _annotations = None if self.annotations == False else [{
                'text': "Source: Coin Metrics Network Data Pro",
                'font': {
                    'size': 12,
                    'color': 'black',
                    },
                'showarrow': False,
                'align': 'left',
                'valign': 'top',
                'x': -0.04,
                'y': 1.1025,
                'xref': 'paper',
                'yref': 'paper',
            }]
        background_color = '#F5F5F5'
        y_axis = {}
        self.fig.update_layout(
            title={
                'text': self.title,
                'font': {
                    'family': 'Roboto',
                    'size': 24
                }
            },
            font = {
                'family': 'Roboto'
            },
            xaxis = {
                'showgrid' : False
            },
            yaxis= y_axis,
            # yaxis2= {
            #     'side': 'right',
            #     # 'overlaying': 'y'
            # },
            showlegend=self.showlegend,
            paper_bgcolor = background_color,
            plot_bgcolor = background_color,
            legend= {
                'bgcolor': background_color, 
                'xanchor': 'center',
                'yanchor': 'top',
                'x': .5,
                'y': -.1,
                'orientation': 'h'
            },
            annotations= _annotations
        )

        if self.stacked == True:
            self.fig.update_layout(
                yaxis = {'ticksuffix': '%', 'side': 'left'},
             )
    
        if self.growth == True:
            self.fig.update_layout(
                yaxis = {'tickformat': ',.0%', 'side': 'left'},
             )

        if self.y_log == True:
            self.fig.update_layout(
                yaxis_type = 'log'
             )

        if self.y2_columns != None and self.y2_log == True:
            self.fig.update_layout(
                yaxis2_type = 'log'
             )

    def run(self):
        ### TODO: Add in y2_columns to DF
        if self.slice_to_df_start == True:
            # chart_df = pd.concat([self.df[self.y_columns], self.df[self.y2_columns]], axis=1, sort=True)
            # self.df = SliceDFStart().transform(chart_df)
            self.df = SliceDFStart().transform(chart_df[self.y_columns])
        if self.seven_day_rolling_average == True:
            self.df= RollingAverage(number_of_days=7).transform(self.df)
            self.df = self.df.iloc[7:]
        if self.growth == True:
            self.df= PercentGrowth(input_columns='all').transform(self.df)
        if self.start == True or self.end == True:
            self.df = DatePicker(start=self.start, end=self.end).transform(self.df)
        if self.date_window:
            self.df = DateWindow(date_window=self.date_window).transform(self.df)
        self.y_columns = [column for column in self.y_columns if column in list(self.df.columns) ]
        ### TODO: Figure out a better way of handling 'map to human readable'
        # self.y_columns = self.map_column_names_to_human_readable(list(self.y_columns))
        # self.df.columns = self.map_column_names_to_human_readable(list(self.df.columns))
        self.implement()
        self.update_fig_layout()
        return self

    