from .ReportABC import Report as Rep
from .Sections.FlowsByExchangeSection import FlowsByExchange

class FlowsReport(Rep):
    def __init__(self, report_title:str, api_key:str, assets:[str], currency_type:str='Ntv', start:str=None, end:str=None, staging:bool=False):
        super().__init__(report_title=report_title, api_key=api_key)
        self.assets = assets
        self.currency_type = currency_type
        self.start = start
        self.end = end
        self.staging = staging
    
    def implement_report_sections(self):
        exchanges = [
            'BFX',
            'BNB',
            'BMX',
            'BSP',
            'BTX',
            'GEM',
            'HUO',
            'KRK',
            # 'LBC',
            # 'OKX',
            'POL',
            # 'HIT',
            # 'CEX'
        ]
        sections = [FlowsByExchange(section_title=exchange +' Flows', assets=self.assets, exchange=exchange, currency_type=self.currency_type, api_key=self.api_key, start=self.start, end=self.end, staging=self.staging) for exchange in exchanges]

        self.load_sections(sections)