from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Visualizers.LineChart import LineChart
from ..CM_API import CM_API
import sys

class ValuationPipeline(Pipe):
    def __init__(self, api_key:str, asset:str):
        super().__init__()
        self.api_key = api_key
        self.asset = asset
        
    def implement_pipeline_steps(self):
        valuation_metrics = ['CapRealUSD', 'CapMrktCurUSD','CapMVRVCur']
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, asset=self.asset, metrics=','.join(valuation_metrics))
        transformers = [
            DateNormalizer()
        ]
        visualizers = [
            LineChart(title='Realized Cap', y_axis_columns=['CapRealUSD']),
            LineChart(title='Market Cap', y_axis_columns=['CapMrktCurUSD']),
            LineChart(title='MVRV', y_axis_columns=['CapMVRVCur']),
        ]
        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.load_visualizers(visualizers=visualizers)
