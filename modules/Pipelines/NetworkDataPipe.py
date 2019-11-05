from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..DataLoaders.CM_API import CM_API

class NetworkDataPipe(Pipe):
    def __init__(self, api_key:str, assets:[str], metrics:[str], start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.assets = assets
        self.metrics = metrics
        self.start = start
        self.end = end
        
    def implement_pipeline_steps(self):
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=self.metrics, start=self.start, end=self.end)
        transformers = [
            DateNormalizer(),
            CastToFloats()
        ]

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)