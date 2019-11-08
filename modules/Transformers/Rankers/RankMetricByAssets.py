from ..TransformerABC import Transformer as tabc
import pandas as pd

class RankMetricByAssets(tabc):
    def __init__(self, metric:str):
        self.metric = metric

    def implement_transformation(self, df):
        row = df.loc[df['metric'] == self.metric]
        row = row.drop(columns='metric')
        result = row.T
        result.columns = ['value']
        result.sort_values(by=['value'], inplace=True, ascending=False)
        result.reset_index(inplace=True)
        return result