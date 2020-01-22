from .PipelineABC import Pipeline as Pipe
from .NetworkDataPipe import NetworkDataPipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.StackTableByAssets import StackTableByAssets
from ..Transformers.Aggregators.NetworkDataXDayAverage import NetworkDataXDayAverage
from ..Transformers.Rankers.RankMetricByAssets import RankMetricByAssets
from ..Transformers.PercentChange import PercentChange
from ..Transformers.ConcatDataframeHorizontally import ConcatDataframeHorizontally
from ..DataLoaders.CM_API import CM_API
import pandas as pd

class CastleIslandPipe(Pipe):
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

    def get_top_ten_assets_by_market_cap(self):
        ranking_df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)
        table_df = NetworkDataXDayAverage(number_of_days=8).transform(ranking_df)
        ranked = RankMetricByAssets(metric='CapMrktCurUSD').transform(table_df)
        top_10 = ranked.loc[0:9]
        top_10_assets_by_market_cap = list(top_10['asset'])
        return top_10_assets_by_market_cap

        
    def implement(self):
        top_10_assets_by_market_cap = self.get_top_ten_assets_by_market_cap()
        
        df = NetworkDataPipe(api_key=self.api_key, assets=top_10_assets_by_market_cap, metrics=['CapMrktCurUSD', 'CapRealUSD', 'PriceUSD'], start=self.start, end=self.end).run()

        # one_day_growth_df = PercentChange(number_of_days=1).transform(df)
        seven_day_growth_df = PercentChange(number_of_days=7).transform(df)

        print(seven_day_growth_df[-30:])

        table_metrics = ['PriceUSD', 'PriceUSD.7dGrowth', 'CapMrktCurUSD', 'CapRealUSD']
        table_column_names = ['Asset', 'Price', 'Price 7d', 'Market Cap', 'Realized Cap']

        transformers = [
            DateNormalizer(),
            CastToFloats(),
            # ConcatDataframeHorizontally(df_to_concat=one_day_growth_df),
            ConcatDataframeHorizontally(df_to_concat=seven_day_growth_df),
            StackTableByAssets(metrics=table_metrics, new_column_names=table_column_names)
            
        ]

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.execute_transformers()

        self.df['Price 7d'] = self.df['Price 7d'] * 100
        self.df['Market Cap'] = self.df['Market Cap'] / 1000000000
        self.df['Realized Cap'] = self.df['Realized Cap'] / 1000000000

        self.df.sort_values(by=['Market Cap'], ascending=False, inplace=True)

        mapper =  {
           'Price': '${0:,.2f}',
        #    'Price 24h': '{0:.2f}%',
           'Price 7d': '{0:.2f}%',
           'Market Cap': '${0:,.1f}B',
           'Realized Cap': '${0:,.1f}B'
        }

        self.df.style.format(mapper)
        

        return self.df