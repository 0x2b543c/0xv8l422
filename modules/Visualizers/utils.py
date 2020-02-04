import pandas as pd
import pdb
from .LineChart import LineChart
from .SubPlot import SubPlot

from enum import Enum
class SubplotTitleTypes(Enum):
    ASSETS = 'assets'
    METRICS = 'metrics'
    COLUMNS = 'y_columns'

class ChartType(Enum):
    LINE = 'line'
    SUBPLOT = 'subplot'

class SplitChartsBy(Enum):
    ASSETS = 'assets'
    METRICS = 'metrics'


def convert_assets_and_metrics_to_columns(self, assets:[str], metrics:[str]):
        columns = []
        for asset in assets:
            for metric in metrics:
                columns.append(f'{asset}.{metric}')
        return columns

def check_if_metric_in_df(self, df, asset, metric):
    columns = list(df.columns)


### chart_type either 'line' or 'subplot'
### split_charts_by either 'assets' or 'metrics'
def create_network_data_chart(**kwargs):
    if kwargs['chart_type'] == 'line':
        chart_args = dict(kwargs)
        del chart_args['chart_type']
        chart = LineChart(**chart_args)
    elif kwargs['chart_type'] == 'subplot':
        chart_args = dict(kwargs)
        del chart_args['chart_type']
        # del chart_args['filled_area']
        # del chart_args['stacked']
        chart = SubPlot(**chart_args)
    result = chart.run()
    return result
    
def create_multiple_network_data_charts(**kwargs):
    charts = []
    assets = kwargs['assets']
    metrics = kwargs['metrics']
    if kwargs['split_charts_by'] == 'assets':
        for asset in assets:
            chart_args = dict(kwargs)
            del chart_args['split_charts_by']
            chart_args['assets'] = [asset]
            chart_args['title'] = asset 
            chart = create_network_data_chart(**chart_args)
            charts.append(chart)
    else:
        for metric in metrics:
            chart_args = dict(kwargs)
            del chart_args['split_charts_by']
            chart_args['metrics'] = [metric]
            chart_args['title'] = metric
            chart = create_network_data_chart(**chart_args)
            charts.append(chart)
    return charts



    # chart_type:ChartType, 
    # assets:[str], 
    # metrics:[str], 
    # # split_charts_by:SplitChartsBy,
    # title:str, 
    # x_column:str='index', 
    # y_columns:[str]=None,  
    # y2_columns:[str]=None,  
    # assets:[str]=None, 
    # metrics:[str]=None, 
    # start:str=None, 
    # end:str=None, 
    # growth=None, 
    # seven_day_rolling_average=False, 
    # filled_area:bool=False, 
    # stacked:bool=False,
    # subplot_titles:SubplotTitleTypes=None, 
    # shared_yaxes=False, 
    # showlegend:bool=False, 
    # annotations:bool=False

