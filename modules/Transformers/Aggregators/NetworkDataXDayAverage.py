from ..TransformerABC import Transformer as tabc
import pandas as pd

class NetworkDataXDayAverage(tabc):
    def __init__(self, number_of_days:int=7):
        self.number_of_days = number_of_days

    def implement_transformation(self, df):
        total_number_of_rows = df.shape[0]
        sliced_df = df.iloc[total_number_of_rows-self.number_of_days:]
        sliced_df = sliced_df.apply(pd.to_numeric)
        mean_df = sliced_df.mean(axis=0)
        assets = [asset.split('.')[0] for asset in mean_df.index]
        metrics = [metric.split('.')[1] for metric in mean_df.index]
        result_df = pd.DataFrame({'asset':assets, 'metric':metrics, 'value':mean_df.values})
        piv = result_df.pivot(index='metric', columns='asset', values='value')
        piv.reset_index(inplace=True)
        return piv