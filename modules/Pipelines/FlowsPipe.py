from .PipelineABC import Pipeline as Pipe
from ..Transformers.DateNormalizer import DateNormalizer
from ..Transformers.CastToFloats import CastToFloats
from ..Transformers.Adder import Adder
from ..Transformers.NetCalculator import NetCalculator
from ..Transformers.CumulativeAdder import CumulativeAdder
from ..Transformers.ReplaceValue import ReplaceValue
from ..Transformers.Subtractor import Subtractor
from ..Transformers.PercentChangeExchangeFlows import PercentChangeExchangeFlows
from ..Transformers.InitialValueExtractor import InitialValueExtractor
from ..DataLoaders.CM_API import CM_API

class FlowsPipe(Pipe):
    def __init__(self, api_key:str, exchange:str, assets:[str], start:str=None, end:str=None, staging:bool=False):
        super().__init__()
        self.api_key = api_key
        self.exchange = exchange
        self.assets = assets
        self.asset = assets[0]
        self.start = start
        self.end = end
        self.staging = staging
        
    def implement_pipeline_steps(self):
        metrics = []
        exchange_metrics = ['FlowIn{}Ntv'.format(self.exchange), 'FlowOut{}Ntv'.format(self.exchange), 'Sply{}Ntv'.format(self.exchange)]
        metrics = metrics + exchange_metrics

        
        
        df = CM_API().get_coinmetrics_network_data(api_key=self.api_key, assets=self.assets, metrics=metrics, start=self.start, end=self.end, staging=self.staging)

        net_flow_transformers = [NetCalculator(
            new_column_name=self.asset + '.' + self.exchange + 'NetFlowNtv',positive_column=self.asset + '.' + 'FlowIn{}Ntv'.format(self.exchange),
            negative_column=self.asset + '.' + 'FlowOut{}Ntv'.format(self.exchange))]
   
        cumulative_net_flow_replace_transformers = [ReplaceValue(
            new_column_name=self.asset + '.' + self.exchange + 'ZeroedNetFlowNtv',
            column=self.asset + '.' + self.exchange + 'NetFlowNtv',new_value=0)]

        cumulative_net_flow_transformers = [CumulativeAdder(
            new_column_name=self.asset + '.' + self.exchange + 'CumulativeNetFlowNtv',column=self.asset + '.' + self.exchange + 'ZeroedNetFlowNtv')]

        starting_sply_transformers = [InitialValueExtractor(
            new_column_name=self.asset + '.' + self.exchange + 'StartingSplyNtv',column=self.asset + '.' + 'Sply{}Ntv'.format(self.exchange))]
        
        net_flow_sply_transformers = [Adder(
            new_column_name=self.asset + '.' + self.exchange + 'NetFlowSplyNtv',column_a=self.asset + '.' + self.exchange + 'StartingSplyNtv',
            column_b=self.asset + '.' + self.exchange + 'CumulativeNetFlowNtv')]

        diff_sply_net_flow_transformers = [Subtractor(
            new_column_name=self.asset + '.' + self.exchange + 'DiffSplyNetFlowNtv',
            column_a=self.asset + '.' + self.exchange + 'NetFlowSplyNtv',
            column_b=self.asset + '.' + 'Sply{}Ntv'.format(self.exchange))]

        flow_pct_change_transformers = [PercentChangeExchangeFlows(
            asset=self.asset,
            exchange=self.exchange)]

        diff_pct_change_net_flow_transformers = [Subtractor(
            new_column_name=self.asset + '.' + self.exchange + 'DiffPercentChangeSplyNetFlowNtv',
            column_a=self.asset + '.' + 'Sply{}NtvPercentChange'.format(self.exchange),
            column_b=self.asset + '.' + self.exchange + 'NetFlowNtvPercentChange')]
        
       
        initial_transformers = [
            DateNormalizer(),
            CastToFloats()
        ] 

        transformers = initial_transformers + net_flow_transformers + cumulative_net_flow_replace_transformers + cumulative_net_flow_transformers  + starting_sply_transformers+ net_flow_sply_transformers + flow_pct_change_transformers + diff_sply_net_flow_transformers + diff_pct_change_net_flow_transformers

        self.load_data(df=df)
        self.transformers = []
        self.load_transformers(transformers=transformers)

        