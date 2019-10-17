# Research Infrastucture Class Interfaces

## CMDataFrame

Attributes:
- this.data

Methods:
- loadDataFromCMAPI(data_type str, api_key str, assets str, metrics str, start str, end str)
    - data_type: network, market, real_time, etc.
- loadDataFromPostgres(database str, query str)
    - database: postgres2replica2, etc.
- convertDataToDf()
- cleanDf()
- transformDf(transformation_type str)
    - transformation_type: moving_average, growth_percentage, etc.
- setStartDate(start_date str)
- setEndDate(end_date str)
- renderDf()     
        


## Chart

Attributes:
- this.chart

Methods:
- setChartType(chart_type str)
    - chart_type: line, bar, etc.
- addXAxis
- addYAxis
- setChartColors
- setChartTitle
- renderChart
- exportPNG

## Table

Attributes:
- table
- title

Methods:
- addColumn
- setHeaders
- setTableColors
- setTableTitle
- renderTable
- exportPNG

## Report 

Attributes:
- report
- title

Methods:
- addChart
- setReportColors
- setReportTitle
- renderReport
- exportPNGs

# Kevin's R Class Interfaces

Functions for fetching data from HTTP API and WebSocket API: 

Function parameters include all parameters defined in the API specification as well as additional parameters for specifying the API version (v1, v2, or v3) and environment (staging or production). 


get_coinmetrics_api_discovery(endpoint:str)
    - endpoint=[assets, asset_info, exchanges, exchange_info, markets, market_info, metrics, metrics_info, indexes, indexes_info]
get_coinmetrics_api_network_data()
get_coinmetrics_api_order_book()
get_coinmetrics_api_quotes()
get_coinmetrics_api_real_time_metric_data()
get_coinmetrics_api_reference_rates()
get_coinmetrics_api_candles()
get_coinmetrics_api_rtrr()
get_coinmetrics_api_sma_data()
connect_coinmetrics_api_websocket()
connect_coinmetrics_api_websocket_order_book()
connect_coinmetrics_api_websocket_quotes()
connect_coinmetrics_api_websocket_real_time_metric_data()
connect_coinmetrics_api_websocket_rtrr()
connect_coinmetrics_api_websocket_trades()
construct_coinmetrics_api_http_url()
construct_coinmetrics_api_websocket_url()

Functions for fetching data from database tables: 

These functions construct and execute optimized SQL queries on the database tables. Functions have all relevant parameters used in WHERE clauses as well as additional parameters for schema and whether to EXPLAIN the query (helpful for debugging slow queries). 

Tables get moved around often to different databases and broader redesign of database architecture and technologies is in development, so design will need to be easily updatable. 

get_coinmetrics_candles_data()
get_coinmetrics_forex_rates_data()
get_coinmetrics_network_data()
get_coinmetrics_order_book_data()
get_coinmetrics_reference_rates_data()
get_coinmetrics_rtrr_data()
get_coinmetrics_trades_data()

Functions for interfacing with external APIs: 

get_alexa_info()
get_alexa_traffic()
get_coinapi_assets()
get_coinapi_candles()
get_coinmarketcap_assets()
get_coinmarketcap_candles()
get_coinmarketcap_prices()
get_cryptocompare_assets()
get_cryptocompare_candles()
get_external_candles()
get_external_ticker()
get_fred_observations()
get_nomics_assets()
get_nomics_candles()
get_nomics_prces()
get_similarweb_traffic()

