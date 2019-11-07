from ..TransformerABC import Transformer as tabc
import pandas as pd

class NetworkDataMetricsAggregator(tabc):
    def __init__(self, aggregated_asset_name:str, metrics:[str]=None):
        self.aggregated_asset_name = aggregated_asset_name
        self.metrics = metrics

    def get_unique_metrics(self, columns:[str]):
        metrics = [metric.split('.')[1] for metric in columns]
        metrics = list(set(metrics))
        return metrics

    def filter_df_by_metric(self, metric:str, df):
        df = df.loc[:, df.columns.str.contains(metric)]
        return df

    def implement_transformation(self, df):
        result = pd.DataFrame()
        if self.metrics == None:
            self.metrics = self.get_unique_metrics(list(df.columns))
        for metric in self.metrics:
            metric_df = self.filter_df_by_metric(metric=metric, df=df)
            aggregated = metric_df.agg('sum', axis="columns")
            new_column_name = self.aggregated_asset_name + '.' + metric
            result[new_column_name] = aggregated
        return result