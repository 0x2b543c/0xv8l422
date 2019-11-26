from .PipelineABC import Pipeline as Pipe
from .NetworkDataPipe import NetworkDataPipe
from ..Transformers.CumulativeAdder import CumulativeAdder
from ..Transformers.Divider import Divider
from ..Transformers.CastToFloats import CastToFloats
from ..DataLoaders.CM_API import CM_API

class AdvancedMetricsPipe(Pipe):
    def __init__(self, api_key:str, assets:[str], start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.assets = assets
        self.metrics = [
            'PriceUSD',
            'CapMrktCurUSD',
            'CapRealUSD',
            'SplyCur',
            'RevAllTimeUSD'
        ]
        self.start = start
        self.end = end
        
    def implement(self):
        df = NetworkDataPipe(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end).run()

        cumulative_mrkt_cap_transformers = [
            CumulativeAdder(new_column_name=f'{asset}.CumulativeMrktCap', column=f'{asset}.CapMrktCurUSD') for asset in self.assets
        ]

        # df.reset_index(inplace=True)

        # market_age_transformers = [
        #     Subtractor(new_column_name=f'{asset}.MarketAge', starting_column=f'{asset}.time', subtractor_columns=[starting_column=f'{asset}.time']) for asset in self.assets
        # ]

        realized_price_transformers = [
            Divider(new_column_name=f'{asset}.RealizedPrice', column_a=f'{asset}.CapRealUSD', column_b=f'{asset}.SplyCur') for asset in self.assets
        ]

        realized_to_thermo_transformers = [
            Divider(new_column_name=f'{asset}.RealCapToThermoCap', column_a=f'{asset}.CapRealUSD', column_b=f'{asset}.RevAllTimeUSD') for asset in self.assets
        ]

        mrkt_cap_to_thermo_transformers = [
            Divider(new_column_name=f'{asset}.MrktCapToThermoCap', column_a=f'{asset}.CapRealUSD', column_b=f'{asset}.RevAllTimeUSD') for asset in self.assets
        ]

        transformers = cumulative_mrkt_cap_transformers + realized_price_transformers + realized_to_thermo_transformers + mrkt_cap_to_thermo_transformers

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.execute_transformers()

        return self.df