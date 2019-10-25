import pytest
import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules.CM_API import CM_API as cm
from modules.Transformers.DateNormalizer import DateNormalizer as dn
from modules.Visualizations.LineChart import LineChart as lc
from modules.Visualizations.Table import Table as tbl
from modules.Reports.GenericReport import GenericReport as gr
from modules.Pipelines.GenericPipeline import GenericPipeline as gp

@pytest.mark.curtest
def test_export_report_pngs():
    test_network_data = cm().get_coinmetrics_network_data(api_key='KKzV6V2DTY87v3m1dGZu', asset='eth', metrics='AdrActCnt,TxCnt', start='2019-01-01', end='2019-01-07')
    test_chart = lc(title='test', y_axis_columns=['AdrActCnt'])
    test_chart_2 = lc(title='test 2', y_axis_columns=['TxCnt'])
    test_table = tbl(title='test table', table_headers=['Active Addresses', 'Transaction Count'], table_columns=['AdrActCnt', 'TxCnt'])
    transformers=[dn()]
    visualizations = [test_chart, test_chart_2, test_table]

    test_pipeline = gp(df=test_network_data, transformers=transformers, visualizations=visualizations)

    test_report = gr(report_title='test report', pipelines=[test_pipeline])
    test_report.run_report()