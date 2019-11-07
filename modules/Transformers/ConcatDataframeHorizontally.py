from .TransformerABC import Transformer as tabc
import pandas as pd

class ConcatDataframeHorizontally(tabc):
    def __init__(self, df_to_concat):
        self.df_to_concat = df_to_concat

    def implement_transformation(self, df):
        result = pd.concat([df, self.df_to_concat], axis=1, sort=True)
        return result