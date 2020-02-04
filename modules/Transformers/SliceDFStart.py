from .TransformerABC import Transformer as tabc
import pandas as pd
import pdb
import math

class SliceDFStart(tabc):
    def __init__(self):
        pass


    def implement_transformation(self, df):
        first_row_index = None
        for row in df.iterrows():
            _row_index = row[0]
            _row = row[1].apply(lambda x: math.isnan(x) == False)
            _row = list(filter(lambda x: x == True, list(_row)))
            if first_row_index != None:
                break
            if len(_row) > 0:
                first_row_index = _row_index
            # pdb.set_trace()
        return df.loc[first_row_index:]