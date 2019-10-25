from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint


class Report(ABC):
    def __init__(self, report_title:str, pipelines=[]):
        self.title = report_title
        self.pipelines = pipelines
        self.report_output = {'dfs': [], 'visuals': []}

    @abstractmethod
    def implement_report(self):
        pass

    def render_report_visualizations(self):
        for visual in self.report_output['visuals']:
           visual.fig.show()

    def export_report_as_pngs(self):
        print(' REPORT NAME??', self.__class__.__name__)
        for visual in self.report_output['visuals']:
            file_path = "{}.png".format(visual.title)
            visual.fig.write_image(file_path)
            print('Exported to ', file_path)

    def export_report_as_jupyter_notebook(self):
        ####
        # sourced from: https://stackoverflow.com/questions/13614783/programmatically-add-cells-to-an-ipython-notebook-for-report-generation
        ####
        nb = nbf.new_notebook()
        cells = []
        
        for var in my_list:
            # Assume make_image() saves an image to file and returns the filename
            image_file = make_image(var)
            text = "Variable: %s\n![image](%s)" % (var, image_file)
            cell = nbf.new_text_cell('markdown', text)
            cells.append(cell)

        nb['worksheets'].append(nbf.new_worksheet(cells=cells))

        with open('my_notebook.ipynb', 'w') as f:
                nbf.write(nb, f, 'ipynb')

    def run_report(self):
        self.implement_report()
        # self.render_report_visualizations()
        self.export_report_as_pngs()
