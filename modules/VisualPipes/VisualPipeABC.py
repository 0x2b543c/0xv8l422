from abc import ABC, abstractmethod

class VisualPipe(ABC):
    def __init__(self, api_key:str, visual_type:str, df=None, start:str=None, end:str=None, growth=False, seven_day_rolling_average:bool=False, log_y_axis:bool=False, y2_axis_columns:[str]=None):
        self.api_key = api_key
        self.visual_type = visual_type
        self.df = df
        self.start = start
        self.end = end
        self.growth = growth
        self.seven_day_rolling_average = seven_day_rolling_average
        self.log_y_axis = log_y_axis
        self.y2_axis_columns = y2_axis_columns
        self.chart_data = []
        self.fig = None

    @abstractmethod
    def implement_chart_data(self, df):
        pass

    def load_data(self, df):
        self.df = df

    def load_transformers(self, transformers:list):
        for transformer in transformers:
            self.transformers.append(transformer)

    def execute_transformers(self):
        for transformer in self.transformers:
            self.df = transformer.transform(self.df)

    ## TODO: Update to change figure type/trace type based on chart_type
    def create_fig(self):
        fig = go.Figure()
        for data_trace in self.chart_data:
            fig.add_trace(go.Scatter(data_trace))
        self.fig = fig

    # TODO: Update to load/run optional transfoerms (e.g. growth, rolling avg, etc.)
    def run(self):
        self.implement_chart_data()
        self.create_fig()
        return self.fig

    