from .VisualizerABC import Visualizer as Vis
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math 

class SubPlot(Vis):
    def __init__(self, df, title:str, x_column:str='index', y_columns:[str]=None, assets:[str]=None, metrics:[str]=None, y2_price_trace:bool=False, growth=None, seven_day_rolling_average=None, layout_type:str=None, shared_yaxes=False):
        super().__init__(df=df, title=title, x_column=x_column, y_columns=y_columns, assets=assets, metrics=metrics, growth=growth, seven_day_rolling_average=seven_day_rolling_average)
        self.y2_price_trace = y2_price_trace
        self.x_column = x_column
        self.growth = growth
        self.layout_type = layout_type
        self.shared_yaxes = shared_yaxes

        self.number_of_rows = math.ceil(len(self.y_columns) / 3) 
        self.number_of_rows = self.number_of_rows if self.number_of_rows > 0 else 1
        self.number_of_columns = 3
        self.row_index = 1
        self.column_index = 1
        self.plot_index = 1


    def increment_indexes(self):
        if self.column_index >= self.number_of_columns:
            self.column_index = 1
            self.row_index += 1
        else: 
            self.column_index += 1
        self.plot_index += 1

    def implement(self):
        # last_values = [self.df[column].iloc[self.df[column].size - 1] for column in self.y_columns]
        percent_layout_types = ['growth', 'raw_percent', 'volatility']
        exchange_names_map = {
            'BFX': 'Bitfinex',
            'BMX': 'BitMEX',
            'BNB': 'Binance',
            'BSP': 'Bitstamp',
            'BTX': 'Bittrex',
            'GEM': 'Gemini',
            'HUO': 'Huobi',
            'KRK': 'Kraken',
            'POL': 'Poloniex',

        }
        fig = make_subplots(
            rows=self.number_of_rows, cols=self.number_of_columns,
            shared_xaxes=True,
            shared_yaxes=True if self.shared_yaxes == True else False,
            # horizontal_spacing=0.5,
            # vertical_spacing=0.4,
            ### TITLES FOR NETWORK DATA ###
            # subplot_titles=[column.split('.')[0] + ', ' + ('$' if self.layout_type == 'fees' else '') + str('{:.2f}'.format(round(self.df[column].iloc[self.df[column].size - 1] * (100 if self.layout_type in ['growth', 'volatility'] else 1), 2))) + ('%' if self.layout_type in percent_layout_types else '') if math.isnan(float(self.df[column].iloc[self.df[column].size - 1])) is False else column.split('.')[0] + ', -' for column in self.y_columns],
            ### TITLES FOR EXCHANGE SUPPLY ###
            subplot_titles=[exchange_names_map[column.split('.')[1][4:7]] for column in self.y_columns]
        )
        for column in self.y_columns:
            metric = column.split('.')[1]
            last_val = self.df[column].iloc[self.df[column].size - 1]
            asset = column.split('.')[0]
            if self.layout_type == 'growth':
                line_color = 'green' if last_val >= 0 else 'red'
            else:
                line_color = 'black'
            fig.add_trace(
                go.Scatter(
                    x=self.df.index,
                    y=self.df[column],
                    yaxis='y1',
                    mode="lines",
                    line= {
                    'color': line_color
                    },
                    name=metric
                ),
                row=self.row_index, col=self.column_index
            )

            if self.y2_price_trace == True:
                y_axis_pad = (self.number_of_rows * self.number_of_columns) + self.plot_index
                fig.add_trace(
                    go.Scatter(
                        x=self.df.index,
                        y=self.df[f'{asset}.PriceUSD'],
                        mode="lines",
                        name='PriceUSD',
                        yaxis='y16',
                        line= {
                            'color': 'green'
                        },
                        marker= {
                            'opacity': 0.1
                        }
                    ),
                    row=self.row_index, col=self.column_index
                )

                if self.growth == True:
                    y_axis = {'tickformat': ',.0%'} 
                    # fig.update_layout(yaxis=y_axis)

            self.increment_indexes()
        
        self.fig = fig


