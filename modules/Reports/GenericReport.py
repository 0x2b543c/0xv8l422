from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class GenericReport(Rep):
    def __init__(self, df, report_title:str, pipelines:list=[]):
        super().__init__(report_title=report_title, pipelines=pipelines, visualizations=visualizations, df=df)

    def implement_report(self):
        for pipeline in self.pipelines:
            updated_visualizations = pipeline.run_pipeline()
            self.visualizations =  self.visualizations + updated_visualizations
   
