from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.Adder import Adder
from ..Transformers.NetCalculator import NetCalculator
from ..Transformers.CumulativeAdder import CumulativeAdder
from ..Transformers.ReplaceValue import ReplaceValue
from ..Transformers.Subtractor import Subtractor
from ..Transformers.InitialValueExtractor import InitialValueExtractor
from ..DataLoaders.CM_API import CM_API

class FlowsPipe(Pipe):
    def __init__(self, api_key:str, exchanges:[str], assets:[str], start:str=None, end:str=None):
        super().__init__()
        self.api_key = api_key
        self.exchanges = exchanges
        self.assets = assets
        self.asset = assets[0]
        self.start = start
        self.end = end
        
    def implement_pipeline_steps(self):
        metrics = []
        for exchange in self.exchanges:
            exchange_metrics = ['FlowIn{}Ntv'.format(exchange), 'FlowOut{}Ntv'.format(exchange), 'Sply{}Ntv'.format(exchange)]
            metrics = metrics + exchange_metrics

        
        
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=metrics, start=self.start, end=self.end)

        net_flow_transformers = [NetCalculator(
            new_column_name=self.asset + '.' + exchange + 'NetFlowNtv',positive_column=self.asset + '.' + 'FlowIn{}Ntv'.format(exchange),
            negative_column=self.asset + '.' + 'FlowOut{}Ntv'.format(exchange)) for exchange in self.exchanges]
   
        cumulative_net_flow_replace_transformers = [ReplaceValue(
            new_column_name=self.asset + '.' + exchange + 'ZeroedNetFlowNtv',
            column=self.asset + '.' + exchange + 'NetFlowNtv',new_value=0) for exchange in self.exchanges]

        cumulative_net_flow_transformers = [CumulativeAdder(
            new_column_name=self.asset + '.' + exchange + 'CumulativeNetFlowNtv',column=self.asset + '.' + exchange + 'ZeroedNetFlowNtv') for exchange in self.exchanges]

        starting_sply_transformers = [InitialValueExtractor(
            new_column_name=self.asset + '.' + exchange + 'StartingSplyNtv',column=self.asset + '.' + 'Sply{}Ntv'.format(exchange)) for exchange in self.exchanges]
        
        net_flow_sply_transformers = [Adder(
            new_column_name=self.asset + '.' + exchange + 'NetFlowSplyNtv',column_a=self.asset + '.' + exchange + 'StartingSplyNtv',
            column_b=self.asset + '.' + exchange + 'CumulativeNetFlowNtv') for exchange in self.exchanges]

        diff_sply_net_flow_transformers = [Subtractor(
            new_column_name=self.asset + '.' + exchange + 'DiffSplyNetFlowNtv',
            column_a=self.asset + '.' + exchange + 'NetFlowSplyNtv',
            column_b=self.asset + '.' + 'Sply{}Ntv'.format(exchange)) for exchange in self.exchanges]
        
       
        initial_transformers = [
            DateNormalizer(),
            CastToFloats()
        ] 

        transformers = initial_transformers + net_flow_transformers + cumulative_net_flow_replace_transformers + cumulative_net_flow_transformers  + starting_sply_transformers+ net_flow_sply_transformers + diff_sply_net_flow_transformers

        self.load_data(df=df)
        self.load_transformers(transformers=transformers)