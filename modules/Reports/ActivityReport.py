from .ReportABC import Report as Rep
from ..Pipelines.NetworkDataIndividualLineCharts import NetworkDataIndividualLineChartsPipe

class ActivityReport(Rep):
    def __init__(self, report_title:str, api_key:str, asset:str):
        super().__init__(report_title=report_title)
        self.api_key = api_key
        self.asset = asset

    def implement_plumbing(self):
        activity_metrics = [
            'AdrActCnt',
            'AdrBalUSD10Cnt',
            'AdrBal1in1BCnt',
            'SplyAct30d',
            'SplyAct1yr',
            'BlkSizeByte'
        ]
        self.load_pipelines([
            NetworkDataIndividualLineChartsPipe(api_key=self.api_key, asset=self.asset, metrics=activity_metrics)
        ])
        
