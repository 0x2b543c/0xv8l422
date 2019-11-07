from .PipelineABC import Pipeline as Pipe
from .NetworkDataPipe import NetworkDataPipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.ConcatDataframeHorizontally import ConcatDataframeHorizontally
from ..Transformers.Aggregators.NetworkDataMetricsAggregator import NetworkDataMetricsAggregator
from ..DataLoaders.CM_API import CM_API

class ERCsAggregatedPipe(Pipe):
    def __init__(self, api_key:str, ERCs:[str]=None, metrics:[str]=None, start:str=None, end:str=None, staging:bool=False, aggregate_ERCs:bool=False):
        super().__init__()
        self.api_key = api_key
        self.ERC_stablecoins = ['dai', 'gusd', 'tusd', 'usdc', 'pax', 'usdt_eth']
        self.ERC_exchange_tokens = ['bnb', 'ht', 'leo_eth']
        self.default_ERCs = ['ant', 'bat', 'cennz', 'ctxc', 'cvc', 'fun', 'link', 'loom','gno', 'gnt', 'icn', 'knc', 'lrc', 'mana', 'mkr', 'omg', 'pay', 'poly', 'powr', 'ppt', 'qash','rep', 'salt', 'srn', 'veri', 'wtc', 'zrx'] + self.ERC_stablecoins
        self.default_metrics = ['AdrActCnt', 'AdrBal1in1BCnt','AdrBalUSD10Cnt','CapMrktCurUSD', 'CapRealUSD','IssTotNtv', 'TxCnt', 'TxTfrCnt', 'TxTfrValAdjUSD', 'VtyDayRet30d']
        self.ERCs = self.default_ERCs if ERCs == None else ERCs
        self.metrics = self.default_metrics if metrics == None else metrics
        self.start = start
        self.end = end
        self.staging = staging
        self.aggregate_ERCs = aggregate_ERCs

    def implement_pipeline_steps(self):
        ercs_df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.ERCs, metrics=self.metrics, start=self.start, end=self.end, staging=self.staging)

        eth_df = NetworkDataPipe(api_key=self.api_key, assets=['eth'], metrics=self.metrics, start=self.start, end=self.end).run_pipeline().get_data()

        transformers = [
            DateNormalizer(),
            CastToFloats()
        ]

        if self.aggregate_ERCs == True:
            transformers = transformers + [
                NetworkDataMetricsAggregator(aggregated_asset_name='ERC-20'),
                ConcatDataframeHorizontally(df_to_concat=eth_df)
            ]

        self.load_data(df=ercs_df)
        self.load_transformers(transformers=transformers)
        