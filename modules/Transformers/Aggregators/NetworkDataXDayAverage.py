from ..TransformerABC import Transformer as tabc
import pandas as pd

class NetworkDataXDayAverage(tabc):
    def __init__(self, number_of_days:int=7):
        self.number_of_days = number_of_days

    def implement_transformation(self, df):
        total_number_of_rows = df.shape[0]
        sliced_df = df.iloc[total_number_of_rows-self.number_of_days:]
        series = sliced_df.agg("mean", axis="index")
        assets = [asset.split('.')[0] for asset in series.index]
        metrics = [metric.split('.')[1] for metric in series.index]
        df = pd.DataFrame({'asset':assets, 'metric':metrics, 'value':series.values})
        piv = df.pivot(index='metric', columns='asset', values='value')
        piv.reset_index(inplace=True)
        return piv