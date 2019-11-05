from .SectionABC import Section
from ...Pipelines.NetworkDataPipe import NetworkDataPipe
from ...Pipelines.FlowsPipe import FlowsPipe
from ...Visualizers.LineChartAssetByMetrics import LineChartAssetByMetrics
from ...Visualizers.LineChart import LineChart

class FlowsByExchange(Section):
    def __init__(self, section_title:str, assets:[str], exchange:str, currency_type:str, api_key:str, start:str=None, end:str=None, staging:bool=False):
        super().__init__(section_title=section_title, api_key=api_key)
        self.assets = assets
        self.exchange = exchange
        self.currency_type = currency_type
        self.staging = staging
        self.start = start
        self.end = end

    def implement_section(self):
        if self.currency_type not in ['USD', 'Ntv']:
            print('currency_type must be USD or Ntv')
        
        inflow_metric = 'FlowIn' + self.exchange + self.currency_type
        outlfow_metric = 'FlowOut' + self.exchange + self.currency_type
        flow_metrics = [inflow_metric, outlfow_metric]
        supply_metrics = ['Sply' + self.exchange + self.currency_type, self.exchange + 'NetFlowSply' + self.currency_type]
        
        all_metrics = flow_metrics + supply_metrics

        flow_visualizers = [LineChartAssetByMetrics(title=self.exchange + ' Exchange Inflow and Outflow ' + self.currency_type, asset=asset, metrics=flow_metrics) for asset in self.assets]

        net_flow_visualizer = [LineChart(title=self.exchange + ' Net Flow ' + self.currency_type, y_axis_columns=[asset + '.' + self.exchange + 'NetFlow' + self.currency_type]) for asset in self.assets]
        
        supply_visualizer = [LineChartAssetByMetrics(title=self.exchange + ' Exchange Supply ' + self.currency_type, asset=asset, metrics=supply_metrics) for asset in self.assets]

        diff_sply_visualizer = [LineChart(title=self.exchange + ' Diff b/w Net Flow Sply and Sply ' + self.currency_type, y_axis_columns=[asset + '.' + self.exchange + 'DiffSplyNetFlow' + self.currency_type]) for asset in self.assets]

        percent_change_visualizers =[LineChart(title=self.exchange + ' Net Flow % Change vs Sply % Change ' + self.currency_type, y_axis_columns=[asset + '.' + self.exchange + 'NetFlowNtvPercentChange', asset + '.' + 'Sply' + self.exchange + 'NtvPercentChange']) for asset in self.assets]
        
        diff_net_flow_visualizer = [LineChart(title=self.exchange + ' (Sply % Change) - (Net Flow % Change) ' + self.currency_type, y_axis_columns=[asset + '.' + self.exchange + 'DiffPercentChangeSplyNetFlow' + self.currency_type]) for asset in self.assets]



        pipe = FlowsPipe(api_key=self.api_key, exchange=self.exchange, assets=self.assets, start=self.start, end=self.end, staging=self.staging)


        pipe.load_visualizers(
            diff_net_flow_visualizer + 
            # percent_change_visualizers + 
            supply_visualizer +
            flow_visualizers + 
            net_flow_visualizer
            )
    
        self.load_pipelines([pipe])
        