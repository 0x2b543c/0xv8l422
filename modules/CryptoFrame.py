import pandas as pd

class CryptoFrame():
    def __init__(self):
       self.cf = pd.DataFrame()

    def transform_dates_to_yyyy_mm_dd(self, column:str='time'):
        pass


    def transform_ratio(self, ratio_name:str, column_a:str, column_b:str):
        self.cf[ratio_name] = self.cf[column_a] / self.cf[column_b]
