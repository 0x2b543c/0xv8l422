from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class UsageReport(Rep):
    def __init__(self, report_title:str):
        super().__init__(report_title=report_title)

    def implement_plumbing(self):
        pass