from abc import ABC, abstractmethod
import pandas as pd

class Report(ABC):
    def __init__(self, df, report_title:str, transformers=[], visualizations=[]):
       self.df = df
       self.transformers = transformers
       self.visualizations = visualizations

    @abstractmethod
    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)
    
    @abstractmethod
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

    def export_report(self, export_type:str):
        if export_type == 'png':
            for visualization in self.visualizations:
                visualization.export_as_png(df=self.df, file_name=visualization.title)
        else: 
            print('Incorrect export type')

    def run_report(self):
        self.load_data(df)
        self.execute_transformers()
        self.render_visualizations()

