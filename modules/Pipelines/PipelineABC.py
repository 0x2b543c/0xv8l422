from abc import ABC, abstractmethod
import pandas as pd

class Pipeline(ABC):
    def __init__(self, df=None, transformers:list=[]):
       self.df = df
       self.transformers = transformers

    @abstractmethod
    def implement(self):
        pass

    def load_data(self, df):
        self.df = df

    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)

    def execute_transformers(self):
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    def reset_pipe(self):
        self.df = None

    def run(self):
        return self.implement()

