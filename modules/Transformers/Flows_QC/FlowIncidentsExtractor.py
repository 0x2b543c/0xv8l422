from ..TransformerABC import Transformer as tabc
import pandas as pd

class FlowIncidentsExtractor(tabc):
    def __init__(self, asset:str, exchange:str, percent_difference_threshold:float=.01):
        self.asset = asset
        self.exchange = exchange
        self.percent_difference_threshold = percent_difference_threshold

    def implement_transformation(self, df):
        filtered_df = df.loc[(df[self.asset + '.' + self.exchange + 'DiffPercentChangeSplyNetFlowNtv'] > self.percent_difference_threshold) | (df[self.asset + '.' + self.exchange + 'DiffPercentChangeSplyNetFlowNtv'] < -self.percent_difference_threshold)]


        if filtered_df.empty == False:

            filtered_df.loc[:,'exchange'] = self.exchange
            filtered_df.loc[:,'asset'] = self.asset
            filtered_df.loc[:, 'NetFlowPctChange'] = filtered_df[self.asset + '.' + self.exchange + 'NetFlowNtvPercentChange']
            filtered_df.loc[:,'SplyPctChange'] = filtered_df[self.asset + '.' + 'Sply{}NtvPercentChange'.format(self.exchange)]
            filtered_df.loc[:,'Difference'] = filtered_df[self.asset + '.' + self.exchange + 'DiffPercentChangeSplyNetFlowNtv']

        new_columns = ['exchange', 'asset', 'NetFlowPctChange', 'SplyPctChange', 'Difference']
        old_columns = list(set(filtered_df.columns).difference(set(new_columns)))
        filtered_df.drop(columns=old_columns, inplace=True)

        return filtered_df