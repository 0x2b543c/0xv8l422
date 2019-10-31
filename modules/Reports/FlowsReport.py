from .ReportABC import Report as Rep
from .Sections.FlowsByExchangeSection import FlowsByExchange

class FlowsReport(Rep):
    def __init__(self, report_title:str, api_key:str, assets:[str], currency_type:str='Ntv'):
        super().__init__(report_title=report_title, api_key=api_key)
        self.assets = assets
        self.currency_type = currency_type
    
    def implement_report_sections(self):
        exchanges = [
            'BFX',
            'BNB',
            'BMX'
        ]
        sections = [FlowsByExchange(section_title=exchange +' Flows', assets=self.assets, exchange=exchange, currency_type=self.currency_type, api_key=self.api_key) for exchange in exchanges]

        self.load_sections(sections)