from abc import ABC, abstractmethod
import pandas as pd

class Report(ABC):
    def __init__(self, report_title:str, pipelines=[]):
        self.title = report_title
        self.pipelines = pipelines
        self.visualizations = []

    @abstractmethod
    def implement_report(self):
        pass

    def export_report_as_pngs(self, export_type:str):
        for visualization in self.visualizations:
            visualization.export_as_png(df=self.df, file_name=visualization.title)

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

    def run_report(self, export_type):
        self.implement_report()
        if export_type == 'png':
            self.export_report_as_pngs()
