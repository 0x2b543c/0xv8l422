from abc import ABC, abstractmethod

class DataSource(ABC):
    def __init__(self, id:str, title:str, data_pipe):
        self.id = id
        self.title = title
        self.data_pipe = data_pipe
        self.df = None