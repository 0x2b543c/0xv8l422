from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint
from pathlib import Path


class Report(ABC):
    def __init__(self, title:str, api_key:str, start:str=None, end:str=None):
        self.title = title
        self.api_key = api_key
        self.start = start
        self.end = end
        self.dfs = []
        self.visuals = []

    @abstractmethod
    def implement(self):
        pass

    def load_data_sources(self, data_sources:list):
        pass

    def load_visual(self, visuals):
        self.visuals = visuals

    def add_data_source(self, data_source):
        self.data_sources[data_source['id']] = data_source

    def get_dfs(self):
        return self.dfs

    def format_y_axis_as_percent(self):
        for visual in self.visuals:
            visual.fig.update_layout(yaxis= {'tickformat': ',.0%'})

    def render_visualizations(self, section:str=None):
        if section is not None:
            section_visuals = [visual for visual in self.visuals if visual.section == section]
            for visual in section_visuals:
                visual.show()
        else:
            for visual in self.visuals:
                visual.show()

    def export_report_as_pngs(self):
        for visual in self.visuals:
            file_path = str(Path(__file__).parent.parent.parent) + '/pngs/{}.png'.format(visual.title)
            # file_path = "/pngs/{}.png".format(visual.title)
            visual.fig.write_image(file_path)
            print('Exported to ', file_path)

    def reset_report_output(self):
        self.dfs = []
        self.visuals = []

    def run(self):
        self.implement()
        return self

