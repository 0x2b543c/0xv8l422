from abc import ABC, abstractmethod
import pandas as pd

class Pipeline(ABC):
    def __init__(self, df=None, transformers:list=[], visualizers:list=[]):
       self.df = df
       self.transformers = transformers
       self.visualizers = visualizers
       self.visuals = []

    @abstractmethod
    def implement_pipeline_steps(self):
        pass

    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)
    
    def load_visualizers(self, visualizers:list):
        self.visualizers = visualizers
    
    def load_data(self, df):
        self.df = df

    def get_data(self):
        return self.df

    def execute_transformers(self):
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    def execute_visualizers(self):
        for visualizer in self.visualizers:
            self.visuals.append(visualizer.create_visual(self.df))

    def reset_pipeline_output(self):
        self.df = None
        self.transformers = []
        self.visualizers = []
        self.visuals = []

    def run_pipeline(self):
        self.reset_pipeline_output()
        self.implement_pipeline_steps()
        self.execute_transformers()
        return self.df

