from abc import ABC, abstractmethod
import pandas as pd

class Pipeline(ABC):
    def __init__(self, df, transformers:list=[], visualizations:list=[]):
       self.df = df
       self.transformers = transformers
       self.visualizations = visualizations

    @abstractmethod
    def implement_pipeline(self, df):
        pass

    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)
    
    def load_visualizations(self, visualizations:list):
        self.visualizations = visualizations
    
    def load_data(self):
        self.df = df

    def get_data(self):
        return self.df

    def execute_transformers(self):
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    def render_visualizations(self):
        for visualization in self.visualizations:
            visualization.render_visualization(self.df)

    def run_pipeline(self):
        self.implement_pipeline(self.df)

