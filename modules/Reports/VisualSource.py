from abc import ABC, abstractmethod

class VisualSource(ABC):
    def __init__(self, id:str, title:str, section:str, data_source_id:str, visual_pipe):
        self.id = id
        self.title = title
        self.section = section
        self.data_source_id = data_source_id
        self.visual_pipe = visual_pipe
        self.fig = None