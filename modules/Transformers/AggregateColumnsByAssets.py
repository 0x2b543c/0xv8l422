from .TransformerABC import Transformer as tabc
from ..DataLoaders.CMDataGroups import CMDataGroups
import pandas as pd
import pdb

from enum import Enum
class AggregationType(Enum):
    SUM = 'sum'
    MEAN = 'mean'

class AggregateColumnsByAssets(tabc):
    def __init__(self, aggregation_type:AggregationType, asset_group_names:[str], metrics:[str]):
        self.aggregation_type = aggregation_type
        self.asset_group_names = asset_group_names
        self.metrics = metrics
        self.asset_groups = CMDataGroups().asset_groups


    def implement_transformation(self, df):
        for asset_group_name in self.asset_group_names:
            _assets = self.asset_groups[asset_group_name]
            for metric in self.metrics:
                columns = []
                for asset in _assets:
                    column = f'{asset}.{metric}'
                    ### Check if metric exists within dataframe
                    if column in list(df.columns):
                        columns.append(column)
                if len(columns) == 0:
                    pass
                new_df = df[columns]
                new_df = new_df.agg(self.aggregation_type, axis="columns")
                df = pd.concat([df, new_df], axis=1, sort=True)
                df.rename(columns={0: f'{asset_group_name}.{metric}'}, inplace=True)
                columns = []
        return df