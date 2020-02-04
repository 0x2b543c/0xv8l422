from .TransformerABC import Transformer as tabc
from ..DataLoaders.CMDataGroups import CMDataGroups
import pandas as pd

class SupplyDistributionNormalizer(tabc):
    def __init__(self, columns:[str]):
        self.columns = columns
        self.metric_groups = CMDataGroups().metric_groups

    def implement_transformation(self, df):
        new_df = df.copy()
        for column in self.columns:
            asset = column.split('.')[0]
            metric = column.split('.')[1]
            metric_group = []
            for group in self.metric_groups.values():
                if metric in group:
                    metric_group = group
            metric_index = metric_group.index(metric)
            if metric_index > 0:
                column_to_subtract = f'{asset}.{metric_group[metric_index - 1]}'
                new_df[column] = df[column] - df[column_to_subtract]
        return new_df