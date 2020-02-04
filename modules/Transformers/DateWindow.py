from .TransformerABC import Transformer as tabc
from .DatePicker import DatePicker
import pandas as pd
from datetime import date, timedelta



from enum import Enum
class DateWindowOptions(Enum):
    _1D = '1d'
    _7D = '7d'
    _30D = '30d'
    _90D = '90d'
    _180D = '180d'
    _1Y = '1y'


class DateWindow(tabc):
    def __init__(self, end:str=None, date_window:DateWindowOptions=None):
        yesterday = date.today() - timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")
        self.end = end if end else yesterday
        self.date_window = date_window       

    def implement_transformation(self, df):
        date_period = int(self.date_window[:-1]) if self.date_window[-1] == 'd' else int(self.date_window[:-1]) * 365
        date_range = pd.date_range(end=self.end, periods=date_period).tolist()
        start_date = date_range[0].strftime("%Y-%m-%d")
        df_slice = DatePicker(start=start_date, end=self.end).transform(df)
        return df_slice