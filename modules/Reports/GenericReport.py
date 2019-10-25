from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class GenericReport(Rep):
    def __init__(self, report_title:str, pipelines:list=[]):
        super().__init__(report_title=report_title, pipelines=pipelines)

    def implement_plumbing(self):
        print('GENERIC REPORT NAME??', self.__class__.__name__)
        pass
   
