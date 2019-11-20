from .PipelineABC import Pipeline as Pipe
from .NetworkDataPipe import NetworkDataPipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.Divider import Divider
from ..Transformers.ConcatDataframeHorizontally import ConcatDataframeHorizontally
from ..Transformers.Aggregators.NetworkDataMetricsAggregator import NetworkDataMetricsAggregator
from ..DataLoaders.CM_API import CM_API

class ERCsCategoriesPipe(Pipe):
    def __init__(self, api_key:str, ERCs:[str]=None, category_names:[str]=None, metrics:[str]=None, start:str=None, end:str=None, staging:bool=False, aggregate_ERCs:bool=False, aggregated_assets_name:str='ERC-20'):
        super().__init__()
        self.api_key = api_key
        self.ERCs = ERCs
        self.default_metrics = ['AdrActCnt', 'AdrBal1in1BCnt','AdrBalUSD10Cnt','CapMrktCurUSD', 'CapRealUSD','IssTotNtv', 'TxCnt', 'TxTfrCnt', 'TxTfrValAdjUSD', 'VtyDayRet30d']
        self.metrics = self.default_metrics if metrics == None else metrics
        self.start = start
        self.end = end
        self.staging = staging
        self.aggregate_ERCs = aggregate_ERCs
        self.aggregate_assets_name = aggregated_assets_name

    def implement_pipeline_steps(self):
        ercs_df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.ERCs, metrics=self.metrics, start=self.start, end=self.end, staging=self.staging)

        # eth_df = NetworkDataPipe(api_key=self.api_key, assets=['eth'], metrics=self.metrics, start=self.start, end=self.end).run_pipeline().get_data()


        transformers = [
            DateNormalizer(),
            CastToFloats()
        ]

        if self.aggregate_ERCs == True:
            transformers = transformers + [
                NetworkDataMetricsAggregator(aggregated_asset_name=self.aggregate_assets_name),
                # ConcatDataframeHorizontally(df_to_concat=eth_df),
                # Divider(column_a='eth.CapMrktCurUSD', column_b=self.aggregate_assets_name + '.CapMrktCurUSD'),
                # Divider(column_a='eth.CapRealUSD', column_b=self.aggregate_assets_name + '.CapRealUSD'),
                # Divider(column_a='eth.TxTfrValAdjUSD', column_b=self.aggregate_assets_name + '.TxTfrValAdjUSD')
            ]

        self.load_data(df=ercs_df)
        self.load_transformers(transformers=transformers)
        