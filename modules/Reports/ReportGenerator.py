from .ReportABC import Report as Rep
from .DataSource import DataSource
from .VisualSource import VisualSource

class ReportGenerator():
    def __init__(self, title:str, data_sources:dict=None, visual_sources:dict=None):
        self.title = title
        self.data_sources = {}
        self.visual_sources = {}

    def add_data_source(self, data_source:DataSource):
        _id = data_source['id']
        self.data_sources[_id] = data_source

    def add_data_sources(self, data_sources:[DataSource]):
        for source in data_sources:
            self.add_data_source(data_source=source)

    def get_data_sources(self) -> dict:
        return self.data_sources

    def add_visual_source(self, visual_source:VisualSource):
        _id = visual_source['id']
        self.visual_sources[_id] = visual_source

    

    
    
        
        
