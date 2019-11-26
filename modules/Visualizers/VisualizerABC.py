from abc import ABC, abstractmethod

class Visualizer(ABC):
    def __init__(self, df, title:str, section:str=None, order:int=None, custom_formatting:str=None):
        self.df = df
        self.title = title
        self.section = section
        self.order = order
        self.custom_formatting = custom_formatting
        self.fig = None

    @abstractmethod
    def implement(self, df):
        pass

    def show(self):
        # TODO: Put in check for visual type (e.g. Plotly, Matplot, etc.)
        return self.fig.show()

    def export(self):
        pass

    def update_fig_layout(self):
        background_color = '#F5F5F5'
        self.fig.update_layout(
            title={
                'text': self.title,
                'font': {
                    'family': 'Roboto',
                    'size': 24
                }
            },
            font = {
                'family': 'Roboto'
            },
            xaxis = {
                'showgrid' : False
            },
            # yaxis= {
            #     'tickformat': ',.0%',
            # },
            paper_bgcolor = background_color,
            plot_bgcolor = background_color,
            legend= {
                'bgcolor': background_color, 
                'xanchor': 'center',
                'yanchor': 'top',
                'x': .5,
                'y': 1.05,
                'orientation': 'h'
            },
            annotations= [{
                'text': "Source: Coin Metrics Network Data Pro",
                'font': {
                    'size': 12,
                    'color': 'black',
                    },
                'showarrow': False,
                'align': 'left',
                'valign': 'top',
                'x': -0.04,
                'y': 1.1025,
                'xref': 'paper',
                'yref': 'paper',
            }]
        )


    def run(self):
        self.implement()
        self.update_fig_layout()
        return self

    