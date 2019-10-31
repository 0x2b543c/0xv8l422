from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint
from pathlib import Path


class Section(ABC):
    def __init__(self, section_title:str, api_key:str):
        self.title = section_title
        self.api_key = api_key
        self.pipelines = []

    @abstractmethod
    def implement_section(self):
        pass

    def load_pipelines(self, pipelines:list):
        for pipe in pipelines:
            self.pipelines.append(pipe)

    def update_section(self):
        self.implement_section()
        return self
