from .ReportABC import Report as Rep
from ..Pipelines.ValuationPipeline import ValuationPipeline

class ValuationReport(Rep):
    def __init__(self, report_title:str, api_key:str, asset:str):
        super().__init__(report_title=report_title)
        self.api_key = api_key
        self.asset = asset

    def implement_plumbing(self):
        self.load_pipelines([
            ValuationPipeline(api_key=self.api_key, asset=self.asset)
        ])
        
    def set_jupyter_notebook_cells(self):
        self.jupyter_notebook_cells = ["""\
            %matplotlib inline
            import sys
            sys.path.append('/workspace')
            from IPython.display import clear_output
            from modules.Reports.ValuationReport import ValuationReport
            """,
            """\
            clear_output()
            api_key = 'KKzV6V2DTY87v3m1dGZu'
            asset = 'eth'
            report_title='Valuation Report'
            report = ValuationReport(report_title=report_title, api_key=api_key, asset=asset)
            report.run_report(export_types=['figures'])
            """
        ]
