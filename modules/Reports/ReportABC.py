from abc import ABC, abstractmethod
import pandas as pd
import nbformat as nbf
from random import randint


class Report(ABC):
    def __init__(self, report_title:str, pipelines=[]):
        self.title = report_title
        self.pipelines = pipelines
        self.report_output = {'dfs': [], 'visualizations': []}

    @abstractmethod
    def implement_report(self):
        pass

    def render_report_visualizations(self):
        for visualization in self.report_output['visualizations']:
           visualization.show()

    def export_report_as_pngs(self):
        print('REPORT NAME??', self.__class__.__name__)
        for visualization in self.report_output['visualizations']:
            file_path = "{}.png".format('yrp' + str(randint(1, 1000000000)))
            visualization.write_image(file_path)
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
