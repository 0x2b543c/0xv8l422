from .ReportABC import Report as Rep
from ..Visualizers.LineChartMetricByAssets import LineChartMetricByAssets
from .ReportDataSource import ReportDataSource
from ..Pipelines.NetworkDataPipe import NetworkDataPipe

class CoinbaseReport(Rep):
    def __init__(self, title:str, api_key:str, asset:str, start:str=None, end:str=None):
        super().__init__(title=title, api_key=api_key, start=start, end=end)
        self.api_key = api_key
        self.asset = asset

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
            'CapMVRVCur'
        ]

        usage_metrics = [
            'AdrActCnt',
            'TxCnt',
            # 'BlkSizeByte'
            'AdrBalUSD10Cnt',
            'AdrBalUSD1MCnt',
            'SplyAct30d'
        ]

        all_metrics = economic_metrics + valuation_metrics + usage_metrics

        df = NetworkDataPipe(api_key=self.api_key, assets=['btc', 'eth'], metrics=all_metrics, start=self.start).run()

        valuation_visuals = [
            LineChartMetricByAssets(_id=1, df=df, title=self.asset + ' ' + metric, metric=metric, assets=[self.asset], section='valuation').run() for metric in valuation_metrics
        ]

        economic_visuals = [
            LineChartMetricByAssets(_id=1, df=df, title=self.asset + ' ' + metric, metric=metric, assets=[self.asset], section='economics').run() for metric in economic_metrics
        ]

        usage_visuals = [
            LineChartMetricByAssets(_id=1, df=df, title=self.asset + ' ' + metric, metric=metric, assets=[self.asset], section='usage').run() for metric in usage_metrics
        ]

        all_visuals = valuation_visuals + economic_visuals + usage_visuals

        self.load_visual(all_visuals)
        
