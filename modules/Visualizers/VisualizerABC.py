from abc import ABC, abstractmethod

class Visualizer(ABC):
    def __init__(self, title:str):
        self.title = title
        self.fig = None

    @abstractmethod
    def implement_visualization(self, df):
        pass

    def create_visual(self, df):
        background_color = '#F5F5F5'
        self.implement_visualization(df)
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
            yaxis= {
                'tickformat': ',.0%',
            },
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
        return self

    