import pytest
import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules.DataLoaders.CM_API import CM_API as cm
from modules.Transformers.DateNormalizer import DateNormalizer as dn
from modules.Visualizers.LineChart import LineChart as lc
from modules.Visualizers.Table import Table as tbl
from modules.Reports.GenericReport import GenericReport as gr
from modules.Pipelines.GenericPipeline import GenericPipeline as gp
from modules.Reports.ValuationReport import ValuationReport
from modules.Reports.ActivityReport import ActivityReport
from modules.Reports.EconomicsReport import EconomicsReport
from modules.Reports.NDPGrowthComparison import NDPGrowthComparison
from modules.Reports.FlowsReport import FlowsReport


def test_export_report_pngs():
    test_network_data = cm().get_coinmetrics_network_data(api_key='KKzV6V2DTY87v3m1dGZu', asset='eth', metrics='AdrActCnt,TxCnt', start='2019-01-01', end='2019-01-07')
    test_chart = lc(title='test', y_axis_columns=['AdrActCnt'])
    test_chart_2 = lc(title='test 2', y_axis_columns=['TxCnt'])
    test_table = tbl(title='test table', table_headers=['Active Addresses', 'Transaction Count'], table_columns=['AdrActCnt', 'TxCnt'])
    transformers=[dn()]
    visualizers = [test_chart, test_chart_2, test_table]

    test_pipeline = gp(df=test_network_data, transformers=transformers, visualizers=visualizers)

    test_report = gr(report_title='test report', pipelines=[test_pipeline])
    test_report.run_report()

def test_valuation_report_jupyter_notebook():
    test_report = ValuationReport(report_title='Test Valuation Report', api_key='KKzV6V2DTY87v3m1dGZu', asset='eth')
    test_report.run_report(export_types=['notebook'])

def test_activity_report_jupyter_notebook():
    test_report = ActivityReport(report_title='Test Activity Report', api_key='KKzV6V2DTY87v3m1dGZu', asset='eth')
    test_report.run_report(export_types=['notebook'])

def test_economics_report_jupyter_notebook():
    test_report = EconomicsReport(report_title='Test Economics Report', api_key='KKzV6V2DTY87v3m1dGZu', asset='eth')
    test_report.run_report(export_types=['notebook'])

def test_network_data_growth_report_jupyter_notebook():
    test_report = NDPGrowthComparison(report_title='Test Growth Report', api_key='KKzV6V2DTY87v3m1dGZu', assets=['btc','eth','bch'], metrics=['AdrActCnt','CapRealUSD'])
    test

@pytest.mark.curtest
def test_flows_report_jupyter_notebook():
    test_report = FlowsReport(report_title='Test Flows Report', api_key='KKzV6V2DTY87v3m1dGZu', asset='btc', currency_type='Ntv')
    test_report.run_report(export_types=['notebook'])