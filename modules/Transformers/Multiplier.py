from .TransformerABC import Transformer as tabc
import pandas as pd

class Multiplier(tabc):
    def __init__(self, column:str, multiplier:int):
        self.column = column
        self.multiplier = multiplier

    def implement_transformation(self, df):
        df[self.column] = df[self.column] * self.multiplier
        return df