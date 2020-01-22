from .VisualPipeABC import VisualPipe
from ..Transformers.Aggregators.NetworkDataMetricsAggregator import NetworkDataMetricsAggregator
from ..DataLoaders.CM_API import CM_API

class NetworkDataVisualPipe(VisualPipe):
    def __init__(self, api_key:str, df=df, assets:[str], metrics:[str], start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.assets = assets
        self.metrics = metrics
        self.start = start
        self.end = end
        self.df = df
        self.chart_data = []

    def implement_chart_data(self):
        for asset in self.assets:
            for metric in self.metrics:
                _chart_data = {
                    'x': self.df.index,
                    'y': self.df[f'{asset}.{metric}']
                    'mode': 'lines',
                    'name': metric,
                    # 'stackgroup'='one',
                    # 'groupnorm'='percent',
                    # 'fill'='tonexty'
                }
                self.chart_data.append(_chart_data)

    def implement(self):
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)

        transformers = [
            DateNormalizer(),
            CastToFloats()
        ]

        if self.aggregate == True:
            transformers.append(NetworkDataMetricsAggregator(aggregated_asset_name=self.aggregated_assets_name))

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.execute_transformers()

        return self.df