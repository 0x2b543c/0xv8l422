from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..DataLoaders.CM_API import CM_API

class CastleIsland(Pipe):
    def __init__(self, api_key:str,start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.assets = [
            'ada',
            'bat',
            'bch',
            'bnb_mainnet',
            'bsv',
            'btc',
            'btg',
            'dai',
            'dash',
            'dcr',
            'doge',
            'eos',
            'etc',
            'eth',
            'grin',
            'ht',
            'leo_eos',
            'leo_eth',
            'link',
            'loom',
            'ltc',
            'mana',
            'mkr',
            'neo',
            'omg',
            'pax',
            'pay',
            'rep',
            'usdc',
            'usdt',
            'usdt_eth',
            'xlm',
            'xmr',
            'xrp',
            'zec',
            'zrx'
            ]
        self.metrics = ['CapMrktCurUSD']
        self.start = start
        self.end = end
        
    def implement_pipeline_steps(self):
        
        ranking_df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)
        table_df = NetworkDataXDayAverage(number_of_days=7).transform(ranking_df)
        ranked = RankMetricByAssets(metric='CapMrktCurUSD').transform(table_df)
        top_10 = ranked.loc[0:9]
        top_10_assets = list(top_10['asset'])

        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=top_10_assets, metrics=['CapMrktCurUSD', 'PriceUSD'], start=self.start, end=self.end)

        transformers = [
            DateNormalizer(),
            CastToFloats(),
            PercentGrowthXoverX(input_column='')
        ]

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)