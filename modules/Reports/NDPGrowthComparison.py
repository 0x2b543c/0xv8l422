from .ReportABC import Report as Rep
from ..Pipelines.NetworkDataGrowth import NetworkDataGrowthPipe

class NDPGrowthComparison(Rep):
    def __init__(self, report_title:str, api_key:str, assets:[str], metrics:[str], start:str=None, end:str=None):
        super().__init__(report_title=report_title)
        self.api_key = api_key
        self.assets = assets
        self.metrics = metrics
        self.start = start
        self.end = end

    def implement_plumbing(self):
        self.load_pipelines([
            NetworkDataGrowthPipe(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)
        ])
        