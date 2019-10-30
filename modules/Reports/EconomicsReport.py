from .ReportABC import Report as Rep
from ..Pipelines.NetworkDataIndividualLineCharts import NetworkDataIndividualLineChartsPipe

class EconomicsReport(Rep):
    def __init__(self, report_title:str, api_key:str, asset:str):
        super().__init__(report_title=report_title)
        self.api_key = api_key
        self.asset = asset

    def implement_plumbing(self):
        economic_metrics = [
            'TxTfrValAdjUSD',
            'TxTfrCnt',
            'IssContPctAnn',
            'FeeTotUSD',
            'FeeMedUSD',
            'VelActAdj1yr'
        ]
        self.load_pipelines([
            NetworkDataIndividualLineChartsPipe(api_key=self.api_key, asset=self.asset, metrics=economic_metrics)
        ])
        
