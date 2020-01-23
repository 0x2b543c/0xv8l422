import pytest
import sys
import os 
import pandas as pd
import pdb
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules.DataLoaders.CoinMetricsAPI.NetworkDataAPI import NetworkDataAPI as _api
from modules.DataLoaders.CMDataGroups import CMDataGroups
from modules.Transformers.DateNormalizer import DateNormalizer
from modules.Transformers.CastToFloats import CastToFloats
from tests.utils import clean_test_data, log_test_data


def test_get_coinmetrics_network_data():
    testObj = _api()


    api_key = 'X3lotGijS27jky7bhO3t'
    assets = ['btc', 'eth', 'bat', 'dcr', 'xtz']
    metrics = ['AdrActCnt', 'PriceUSD', 'TxCnt']
    start = '2019-01-01'
    end = '2019-01-07'

    result = testObj.get_coinmetrics_network_data(api_key=api_key, assets=assets, metrics=metrics, start=start, end=end)

    dummy_result = pd.read_csv('./tests/test_data/test-network-data.csv')
    dummy_result.set_index('date', inplace=True)

    # pdb.set_trace()

    log_test_data(dummy_result=dummy_result, result=result)

    assert dummy_result.equals(result)

def test_stablecoin_usage_network_data():
    testObj = _api()


    api_key = 'X3lotGijS27jky7bhO3t'
    assets = CMDataGroups().get_asset_groups()['stablecoins']
    metrics = CMDataGroups().get_metric_groups()['usage']
    start = '2019-01-01'
    end = '2019-01-07'
    result = testObj.get_coinmetrics_network_data(api_key=api_key, assets=assets, metrics=metrics, start=start, end=end)
    dummy_result = pd.read_csv('./tests/test_data/stablecoin-usage-data.csv')
    dummy_result.set_index('date', inplace=True)
    dummy_result.index.rename('time', inplace=True)
    dummy_result = DateNormalizer().transform(dummy_result)
    dummy_result = CastToFloats().transform(dummy_result)

    log_test_data(dummy_result=dummy_result, result=result)

    assert dummy_result.equals(result)