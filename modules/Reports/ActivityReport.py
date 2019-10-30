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
        
    def set_jupyter_notebook_cells(self):
        self.jupyter_notebook_cells = ["""\
            %matplotlib inline
            import sys
            sys.path.append('/workspace')
            from IPython.display import clear_output
            from modules.Reports.NetworkDataIndividualLineChartsPipe import NetworkDataIndividualLineChartsPipe
            """,
            """\
            clear_output()
            api_key = 'KKzV6V2DTY87v3m1dGZu'
            asset = 'eth'
            report_title='Activity Report'
            report = NetworkDataIndividualLineChartsPipe(report_title=report_title, api_key=api_key, asset=asset)
            report.run_report(export_types=['figures'])
            """
        ]
