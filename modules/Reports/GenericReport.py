from .ReportABC import Report as Rep
import pandas as pd
import plotly.graph_objects as go

class GenericReport(Rep):
    def __init__(self, df, report_title:str, transformers:list=[], visualizations:list=[]):
        super().__init__(report_title=report_title, transformers=transformers, visualizations=visualizations, df=df)

    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)
    
    def load_visualizations(self, visualizations:list):
        self.visualizations = visualizations
   
