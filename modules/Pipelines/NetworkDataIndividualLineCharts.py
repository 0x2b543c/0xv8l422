from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Visualizers.LineChart import LineChart
from ..DataLoaders.CM_API import CM_API

class NetworkDataIndividualLineChartsPipe(Pipe):
    def __init__(self, api_key:str, assets:[str], metrics:[str]):
        super().__init__()
        self.api_key = api_key
        self.assets = assets
        self.metrics = metrics
        
    def implement_pipeline_steps(self):
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=','.join(self.metrics))
        transformers = [
            DateNormalizer()
        ]
        visualizers = [LineChart(title=metric, y_axis_columns=[metric]) for metric in self.metrics]

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)
        self.load_visualizers(visualizers=visualizers)