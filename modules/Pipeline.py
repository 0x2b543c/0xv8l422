import pandas as pd

class Pipeline():
    def __init__(self, df=None):
       self.df = pd.DataFrame() if df == None else df
       self.transformers = []
       self.visualizations = []

    def load_data(self, df):
        self.df = df

    def get_data(self):
        return self.df

    def load_transformers(self, transformers:list):
        print('TRANSFORMERS', self.transformers)
        for transformer in transformers:
            self.transformers.append(transformer)

    def execute_transformers(self):
        print(self.transformers)
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    def load_visualizations(self, visualizations:list):
        self.visualizations = visualizations

    def print_transformers(self):
        print('TRANSFORMERS', self.transformers)

    def render_visuaalizations(self):
        for visualization in self.visualizations:
            visualization.render_visualization(self.df)

    def export_visualizations(self, export_type:str):
        if export_type == 'png':
            for visualization in self.visualizations:
                pass
            visualization.export_as_png(df=self.df, file_name=visualization.title)
        else: 
            print('Incorrect export type')
            pass 

    def execute_pipeline(self):
        pass




