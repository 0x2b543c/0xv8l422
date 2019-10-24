from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class GenericReport(Rep):
    def __init__(self, report_title:str, pipelines:list=[]):
        super().__init__(report_title=report_title, pipelines=pipelines)

    def implement_report(self):
        for pipeline in self.pipelines:
            pipe_output = pipeline.run_pipeline()
            self.report_output['visualizations'] =  self.report_output['visualizations'] + pipe_output['visualizations']
            self.report_output['dfs'].append(pipe_output['df'])
   
