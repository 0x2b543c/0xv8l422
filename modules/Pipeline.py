import pandas as pd

class Pipeline():
    def __init__(self, df=None):
       self.df = pd.DataFrame() if df == None else df
       self.transformers = []
       self.charts = []

    def load_data(self, df):
        self.df = df

    def get_data(self):
        return self.df

    def load_transformers(self, transformers:list):
        print('TRANSFORMERS', self.transformers)
        for transformer in transformers:
            self.transformers.append(transformer)

    def execute_transformers(self):
        print(self.transformers)
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    def load_charts(self, charts:list):
        self.charts = charts

    def print_transformers(self):
        print('TRANSFORMERS', self.transformers)

    def render_charts(self):
        for chart in self.charts:
            chart.render_chart(self.df)

    def export_charts(self, export_type:str):
        if export_type == 'png':
            for chart in self.charts:
                pass
            chart.export_as_png(df=self.df, file_name=chart.chart_title)
        else: 
            print('Incorrect export type')
            pass 

    def execute_pipeline(self):
        pass




