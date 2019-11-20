from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint
from pathlib import Path


class ReportDataSource(ABC):
    def __init__(self, _id:int, title:str, data_source):
        self._id = _id
        self.title = report_title
        self.data_source = data_source

    def run(self):
        return self.data_source.run()
