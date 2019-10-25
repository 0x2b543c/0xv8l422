from .PipelineABC import Pipeline as Pipe
import pandas as pd
import plotly.graph_objects as go

class GenericPipeline(Pipe):
    def __init__(self, df, transformers:list=[], visualizers:list=[]):
        super().__init__(transformers=transformers, visualizers=visualizers, df=df)

    def implement_pipeline(self, df):
        self.load_data(df)
        self.execute_transformers()
        self.execute_visualizers()
   
