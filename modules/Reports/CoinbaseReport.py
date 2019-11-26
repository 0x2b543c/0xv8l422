from .ReportABC import Report as Rep
from ..Visualizers.LineChartMetricByAssets import LineChartMetricByAssets
from ..Pipelines.NetworkDataPipe import NetworkDataPipe
from ..Transformers.PercentGrowth import PercentGrowth

class CoinbaseReport(Rep):
    def __init__(self, title:str, api_key:str, assets:[str], start:str=None, end:str=None):
        super().__init__(title=title, api_key=api_key, start=start, end=end)
        self.api_key = api_key
        self.assets = assets

    def implement(self):
        economic_metrics = [
            'TxTfrValAdjUSD',
            'TxTfrCnt',
            'IssContPctAnn',
            'FeeTotUSD',
            'FeeMedUSD',
            'VelActAdj1yr'
        ]

        valuation_metrics = [
            'CapRealUSD',
            'CapMrktCurUSD',
            'CapMVRVCur',
            'PriceUSD'
        ]

        usage_metrics = [
            'AdrActCnt',
            'TxCnt',
            # 'BlkSizeByte'
            'AdrBalUSD10Cnt',
            'AdrBalUSD1MCnt',
            'SplyAct30d'
        ]

        security_metrics = [
            'HashRate',
            'DiffMean',
            'RevUSD'
        ]

        all_metrics = economic_metrics + valuation_metrics + usage_metrics + security_metrics

        df = NetworkDataPipe(api_key=self.api_key, assets=self.assets, metrics=all_metrics, start=self.start).run()

        df= PercentGrowth().transform(df)

        valuation_visuals = [
            LineChartMetricByAssets(df=df, title=metric, metric=metric, assets=self.assets, section='valuation').run() for metric in valuation_metrics
        ]

        economic_visuals = [
            LineChartMetricByAssets(df=df, title=metric, metric=metric, assets=self.assets, section='economics').run() for metric in economic_metrics
        ]

        usage_visuals = [
            LineChartMetricByAssets(df=df, title=metric, metric=metric, assets=self.assets, section='usage').run() for metric in usage_metrics
        ]

        security_visuals = [
            LineChartMetricByAssets(df=df, title=metric, metric=metric, assets=self.assets, section='security').run() for metric in security_metrics
        ]

        all_visuals = valuation_visuals + economic_visuals + usage_visuals + security_visuals

        self.load_visual(all_visuals)
        
