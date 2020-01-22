from abc import ABC, abstractmethod
from ..Transformers.PercentGrowth import PercentGrowth
from ..Transformers.RollingAverage import RollingAverage
from pathlib import Path

class Visualizer(ABC):
    def __init__(self, df, title:str, section:str=None, order:int=None, custom_formatting:str=None, growth:str=None, seven_day_rolling_average:str=None):
        self.df = df
        self.title = title
        self.section = section
        self.order = order
        self.custom_formatting = custom_formatting
        self.fig = None
        # Display Options
        # TODO: Add these as params
        self.growth = growth
        self.seven_day_rolling_average = seven_day_rolling_average

        # self.market_share = market_share
        # self.aggregate = aggregate
        # self.aggregated_assets_name = aggregated_assets_name
        # self.log_y_axis = log_y_axis
        # self.y2_axis_columns = y2_axis_columns

    @abstractmethod
    def implement(self, df):
        pass

    def show(self):
        # TODO: Put in check for visual type (e.g. Plotly, Matplot, etc.)
        return self.fig.show()

    def export(self, title:str, repo:str):
        file_path = str(Path(__file__).parent.parent.parent) + '/pngs/{}/{}.png'.format(repo, title)
        # file_path = "/pngs/{}.png".format(visual.title)
        self.fig.write_image(file_path)

    def update_fig_layout(self):
        background_color = '#F5F5F5'
        # y_axis = {'tickformat': ',.0%'} if self.growth == True else {}
        # y_axis = {'tickformat': ',.0%'} 
        # y_axis = {'ticksuffix': '%'}
        # y_axis = {'tickprefix': '$'}
        y_axis = {}
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
            yaxis= y_axis,
            # yaxis2= {
            #     'side': 'right',
            #     # 'overlaying': 'y'
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
            # annotations= [{
            #     'text': "Source: Coin Metrics Network Data Pro",
            #     'font': {
            #         'size': 12,
            #         'color': 'black',
            #         },
            #     'showarrow': False,
            #     'align': 'left',
            #     'valign': 'top',
            #     'x': -0.04,
            #     'y': 1.1025,
            #     'xref': 'paper',
            #     'yref': 'paper',
            # }]
        )

        if self.growth == 'something':
            self.fig.update_layout(
                yaxis2 = {'ticksuffix': '%', 'side': 'left'},
                xaxis2 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis3 = {'ticksuffix': '%', 'side': 'left'},
                xaxis3 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis4 = {'ticksuffix': '%', 'side': 'left'},
                xaxis4 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis5 = {'ticksuffix': '%', 'side': 'left'},
                xaxis5 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis6 = {'ticksuffix': '%', 'side': 'left'},
                xaxis6 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis7 = {'ticksuffix': '%', 'side': 'left'},
                xaxis7 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis8 = {'ticksuffix': '%', 'side': 'left'},
                xaxis8 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis9 = {'ticksuffix': '%', 'side': 'left'},
                xaxis9 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis10 = {'ticksuffix': '%', 'side': 'left'},
                xaxis10 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis11 = {'ticksuffix': '%', 'side': 'left'},
                xaxis11 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis12 = {'ticksuffix': '%', 'side': 'left'},
                xaxis12 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis13 = {'ticksuffix': '%', 'side': 'left'},
                xaxis13 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis14 = {'ticksuffix': '%', 'side': 'left'},
                xaxis14 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis15 = {'ticksuffix': '%', 'side': 'left'},
                xaxis15 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis16 = {'ticksuffix': '%', 'side': 'left'},
                xaxis16 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis17 = {'ticksuffix': '%', 'side': 'left'},
                xaxis17 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis18 = {'ticksuffix': '%', 'side': 'left'},
                xaxis18 = {
                    'showgrid' : False
                }
             )
    
        if self.growth == True:
            self.fig.update_layout(
                yaxis2 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis2 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis3 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis3 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis4 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis4 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis5 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis5 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis6 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis6 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis7 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis7 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis8 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis8 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis9 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis9 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis10 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis10 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis11 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis11 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis12 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis12 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis13 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis13 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis14 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis14 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis15 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis15 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis16 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis16 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis17 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis17 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis18 = {'tickformat': ',.0%', 'side': 'left'},
                xaxis18 = {
                    'showgrid' : False
                }
             )

        if self.growth == 'fees':
            self.fig.update_layout(
                yaxis2 = {'tickprefix': '$', 'side': 'left'},
                xaxis2 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis3 = {'tickprefix': '$', 'side': 'left'},
                xaxis3 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis4 = {'tickprefix': '$', 'side': 'left'},
                xaxis4 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis5 = {'tickprefix': '$', 'side': 'left'},
                xaxis5 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis6 = {'tickprefix': '$', 'side': 'left'},
                xaxis6 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis7 = {'tickprefix': '$', 'side': 'left'},
                xaxis7 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis8 = {'tickprefix': '$', 'side': 'left'},
                xaxis8 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis9 = {'tickprefix': '$', 'side': 'left'},
                xaxis9 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis10 = {'tickprefix': '$', 'side': 'left'},
                xaxis10 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis11 = {'tickprefix': '$', 'side': 'left'},
                xaxis11 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis12 = {'tickprefix': '$', 'side': 'left'},
                xaxis12 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis13 = {'tickprefix': '$', 'side': 'left'},
                xaxis13 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis14 = {'tickprefix': '$', 'side': 'left'},
                xaxis14 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis15 = {'tickprefix': '$', 'side': 'left'},
                xaxis15 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis16 = {'tickprefix': '$', 'side': 'left'},
                xaxis16 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis17 = {'tickprefix': '$', 'side': 'left'},
                xaxis17 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis18 = {'tickprefix': '$', 'side': 'left'},
                xaxis18 = {
                    'showgrid' : False
                }
             )

        if self.growth == 'mvrv':
            self.fig.update_layout(
                yaxis2 = {'side': 'left'},
                xaxis2 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis3 = {'side': 'left'},
                xaxis3 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis4 = {'side': 'left'},
                xaxis4 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis5 = {'side': 'left'},
                xaxis5 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis6 = {'side': 'left'},
                xaxis6 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis7 = {'side': 'left'},
                xaxis7 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis8 = {'side': 'left'},
                xaxis8 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis9 = {'side': 'left'},
                xaxis9 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis10 = {'side': 'left'},
                xaxis10 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis11 = {'side': 'left'},
                xaxis11 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis12 = {'side': 'left'},
                xaxis12 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis13 = {'side': 'left'},
                xaxis13 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis14 = {'side': 'left'},
                xaxis14 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis15 = {'side': 'left'},
                xaxis15 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis16 = {'side': 'left'},
                xaxis16 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis17 = {'side': 'left'},
                xaxis17 = {
                    'showgrid' : False
                }
             )
            self.fig.update_layout(
                yaxis18 = {'side': 'left'},
                xaxis18 = {
                    'showgrid' : False
                }
             )

    def run(self):
        if self.seven_day_rolling_average == True:
            self.df= RollingAverage(number_of_days=7).transform(self.df)
            self.df = self.df.iloc[7:]
        if self.growth == True:
            self.df= PercentGrowth().transform(self.df)
        self.implement()
        self.update_fig_layout()
        return self

    