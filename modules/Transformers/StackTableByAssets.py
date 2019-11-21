from .TransformerABC import Transformer as tabc
import pandas as pd

class StackTableByAssets(tabc):
    def __init__(self, new_column_names:[str], assets:['str']='all', metrics:['str']='all', date:str=None):
        self.assets = assets
        self.metrics = metrics
        self.date = date
        self.new_column_names = new_column_names

    def implement_transformation(self, df):
        result = pd.DataFrame(columns=self.new_column_names)
        
        if self.date == None:
            day_df = df.iloc[-1:]
        else:
            day_df = df.loc[self.date]
        # day_df.reset_index(inplace=True)


        if self.assets == 'all':
            self.assets = list(set([column.split('.')[0] for column in df.columns]))

        for asset in self.assets:
            asset_columns = [f'{asset}.{metric}' for metric in self.metrics ]

            row = day_df[asset_columns]
            row.insert(loc=0, column='asset', value=asset)
            row.columns = self.new_column_names
            result = result.append(row, ignore_index=True, sort=False)

        return result