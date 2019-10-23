from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class GenericReport(Rep):
    def __init__(self, df, report_title:str, transformers:list=[], visualizations:list=[]):
        super().__init__(report_title=report_title, transformers=transformers, visualizations=visualizations, df=df)

    def implement_report(self, df, export:bool=False):
        self.load_data(df)
        self.execute_transformers()
        self.render_visualizations()
        if export == True:
            self.export_report_as_pngs()
