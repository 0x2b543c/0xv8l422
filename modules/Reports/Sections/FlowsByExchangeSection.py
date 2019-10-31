from .SectionABC import Section
from ...Pipelines.NetworkDataPipe import NetworkDataPipe
from ...Visualizers.LineChartAssetByMetrics import LineChartAssetByMetrics

class FlowsByExchange(Section):
    def __init__(self, section_title:str, assets:[str], exchange:str, currency_type:str, api_key:str):
        super().__init__(section_title=section_title, api_key=api_key)
        self.assets = assets
        self.exchange = exchange
        self.currency_type = currency_type

    def implement_section(self):
        if self.currency_type not in ['USD', 'Ntv']:
            print('currency_type must be USD or Ntv')
        
        inflow_metric = 'FlowIn' + self.exchange + self.currency_type
        outlfow_metric = 'FlowOut' + self.exchange + self.currency_type
        flow_metrics = [inflow_metric, outlfow_metric]
        supply_metric = ['Sply' + self.exchange + self.currency_type]
        all_metrics = flow_metrics + supply_metric

        flow_visualizers = [LineChartAssetByMetrics(title=self.exchange + ' Exchange Flow ' + self.currency_type, asset=asset, metrics=flow_metrics) for asset in self.assets]
        supply_visualizer = [LineChartAssetByMetrics(title=self.exchange + ' Exchange Supply ' + self.currency_type, asset=asset, metrics=supply_metric) for asset in self.assets]

        pipe = NetworkDataPipe(api_key=self.api_key, assets=self.assets, metrics=all_metrics, start='2019-01-01')
        pipe.load_visualizers(flow_visualizers + supply_visualizer)
    
        self.load_pipelines([pipe])
        