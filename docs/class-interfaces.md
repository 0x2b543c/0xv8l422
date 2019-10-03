# Research Infrastucture Class Interfaces

## CMDataFrame

Attributes:
- data

Methods:
- loadDataFromAPI(data_type str, api_key str, assets str, metrics str, start str, end str)
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
- chart

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
