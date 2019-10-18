import pandas as pd

class CryptoFrame():
    def __init__(self, data=None):
       self.data = pd.DataFrame() if data == None else data

    def load_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def transform_dates_to_yyyy_mm_dd(self, column:str='time'):
        self.data[column] = pd.to_datetime(self.data[column]).dt.strftime('%Y-%m-%d')

    def transform_ratio(self, ratio_name:str, column_a:str, column_b:str):
        pass


