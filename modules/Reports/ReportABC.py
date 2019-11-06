from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint
from pathlib import Path


class Report(ABC):
    def __init__(self, report_title:str, api_key:str):
        self.title = report_title
        self.api_key = api_key
        self.sections = []
        self.dfs = []
        self.visuals = []

    # @abstractmethod
    # def implement_plumbing(self):
    #     pass

    @abstractmethod
    def implement_report_sections(self):
        pass

    def load_sections(self, sections:list):
        for section in sections:
            self.sections.append(section)

    def render_report_visualizations(self):
        for visual in self.visuals:
           visual.fig.show()

    def export_report_as_pngs(self):

        for visual in self.visuals:
            file_path = str(Path(__file__).parent.parent.parent) + '/pngs/{}.png'.format(visual.title)
            # file_path = "/pngs/{}.png".format(visual.title)
            visual.fig.write_image(file_path)
            print('Exported to ', file_path)


    def export_report_as_jupyter_notebook(self):
        ####
        # sourced from: https://nbviewer.jupyter.org/gist/fperez/9716279
        # and
        #  https://stackoverflow.com/questions/13614783/programmatically-add-cells-to-an-ipython-notebook-for-report-generation
        ####
        nb = nbf.v4.new_notebook()
        title_cell = "{report_title}".format(report_title=self.title)
        code_cells = ["""\
            %matplotlib inline
            import sys
            sys.path.append('/workspace')
            from IPython.display import clear_output
            from modules.Reports.{class_name} import {class_name}
            """.format(class_name=self.__class__.__name__),
            """\
            clear_output()
            api_key = 'KKzV6V2DTY87v3m1dGZu'
            assets = ['btc', 'eth', 'ada']
            report_title='{report_title}'
            report = {class_name}(report_title=report_title, api_key=api_key, assets=assets)
            report.run_report(export_types=['figures'])
            """.format(report_title=self.title, class_name=self.__class__.__name__)
        ]

        nb['cells'] = [nbf.v4.new_markdown_cell(title_cell)] + [nbf.v4.new_code_cell(cell) for cell in code_cells]
  
        file_path = str(Path(__file__).parent.parent.parent) + '/notebooks/{}.ipynb'.format(self.title)
        nbf.write(nb,file_path)

    def reset_report_output(self):
        self.dfs = []
        self.visuals = []

    def update_report_output(self):
        self.reset_report_output()
        for section in self.sections:
            section.update_section()
            for pipeline in section.pipelines:
                pipe_output = pipeline.run_pipeline()
                df = pipe_output.get_data()
                visuals = pipe_output.get_visuals()
                self.dfs.append(df)
                self.visuals = self.visuals + visuals

    def run_report(self, export_types:[str]):
        self.implement_report_sections()
        self.update_report_output()
        if 'figures' in export_types:
            self.render_report_visualizations()
        if 'pngs' in export_types:
            self.export_report_as_pngs()
        if 'notebook' in export_types:
            self.export_report_as_jupyter_notebook()

