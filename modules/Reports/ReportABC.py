from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint
from pathlib import Path


class Report(ABC):
    def __init__(self, report_title:str, pipelines=[]):
        self.title = report_title
        self.pipelines = pipelines
        self.jupyter_notebook_cells = []
        self.sections = []
        self.report_output = {'dfs': [], 'visuals': []}

    @abstractmethod
    def implement_plumbing(self):
        pass

    def load_sections(self, sections:list):
        for section in sections:
            self.sections.append(pipeline)

    @abstractmethod
    def set_jupyter_notebook_cells(self):
        pass

    def render_report_visualizations(self):
        for visual in self.report_output['visuals']:
           visual.fig.show()

    def export_report_as_pngs(self):
        for visual in self.report_output['visuals']:
            file_path = "{}.png".format(visual.title)
            visual.fig.write_image(file_path)
            print('Exported to ', file_path)

    def reset_jupyter_notebook_cells(self):
        self.jupyter_notebook_cells = []


    def export_report_as_jupyter_notebook(self):
        ####
        # sourced from: https://nbviewer.jupyter.org/gist/fperez/9716279
        # and
        #  https://stackoverflow.com/questions/13614783/programmatically-add-cells-to-an-ipython-notebook-for-report-generation
        ####
        nb = nbf.v4.new_notebook()
        text = """\
        My first automatic Jupyter Notebook
        This is an auto-generated notebook."""

        nb['cells'] = [
            # nbf.v4.new_markdown_cell(text)
        ]
        self.reset_jupyter_notebook_cells()
        self.set_jupyter_notebook_cells()
        for cell in self.jupyter_notebook_cells:
            new_cell = nbf.v4.new_code_cell(cell)
            nb['cells'].append(new_cell)

        file_path = str(Path(__file__).parent.parent.parent) + '/notebooks/{}.ipynb'.format(self.title)
        nbf.write(nb,file_path)

    def load_pipelines(self, pipelines:list):
        for pipeline in pipelines:
            self.pipelines.append(pipeline)

    def reset_report_output(self):
        self.report_output = {'dfs': [], 'visuals': []}

    def update_report_output(self):
        self.reset_report_output()
        for pipeline in self.pipelines:
            pipe_output = pipeline.run_pipeline()
            self.report_output['visuals'] =  self.report_output['visuals'] + pipe_output.visuals
            self.report_output['dfs'].append(pipe_output.df)

    def run_report(self, export_types:[str]):
        self.implement_plumbing()
        self.update_report_output()
        if 'figures' in export_types:
            self.render_report_visualizations()
        if 'pngs' in export_types:
            self.export_report_as_pngs()
        if 'notebook' in export_types:
            self.export_report_as_jupyter_notebook()

