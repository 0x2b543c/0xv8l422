import pandas as pd

class Pipeline():
    def __init__(self, df=None):
       self.df = pd.DataFrame() if df == None else df
       self.transformers = []

    def load_data(self, df):
        self.df = df

    def get_data(self):
        return self.df

    def load_transformers(self, transformers:list):
        self.transformers = transformers

    def execute_transformers(self):
        for transformer in self.load_transformers:
            self.df = transformer.transform(self.df)

    def execute_pipeline(self):
        pass




