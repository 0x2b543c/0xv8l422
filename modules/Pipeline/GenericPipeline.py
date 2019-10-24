from .PipelineABC import Pipeline as Pipe
import pandas as pd
import plotly.graph_objects as go

class GenericPipeline(Pipe):
    def __init__(self, df, transformers:list=[], visualizations:list=[]):
        super().__init__(transformers=transformers, visualizations=visualizations, df=df)

    def implement_pipeline(self, df):
        self.load_data(df)
        self.execute_transformers()
        self.render_visualizations()
   
