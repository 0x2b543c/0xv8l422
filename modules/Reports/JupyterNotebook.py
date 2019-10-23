from .ReportABC import ReportABC as Rep
import pandas as pd
import plotly.graph_objects as go
from IPython.nbformat import current as nbf

class JupyterNotebook(Rep):
    def __init__(self, chart_title:str, y_axis_columns:[str], x_axis_column:str='time'):
        self.title = None
        self.y_axis_columns = y_axis_columns
        self.x_axis_column = x_axis_column

    def create_report(self, df):
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