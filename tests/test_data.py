import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules import Data as d

def test_init_dataframe():
    testObj = d.Data()
    assert isinstance(testObj.df, pd.DataFrame)

def test_call_coinmetrics_api():
    testObj = d.Data()
    test_params = {
        'metrics': 'AdrActCnt,CapRealUSD,TxCnt',
        'start': '2017-01-01',
        'end': '2017-01-05'
    }
    result = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/assets/eth/metricdata', params = test_params)
    dummy_result = {'metricData': {'metrics': ['AdrActCnt', 'CapRealUSD', 'TxCnt'], 'series': [{'time': '2017-01-01T00:00:00.000Z', 'values': ['13946.0', '734673672.319139817831833516177060007323674', '38730.0']}, {'time': '2017-01-02T00:00:00.000Z', 'values': ['15232.0', '736035521.072371336253635824094185064179384', '39652.0']}, {'time': '2017-01-03T00:00:00.000Z', 'values': ['14868.0', '741146428.959793620825964110400677939075684', '45883.0']}, {'time': '2017-01-04T00:00:00.000Z', 'values': ['18066.0', '749721286.811463913996829494293959461077514', '50673.0']}, {'time': '2017-01-05T00:00:00.000Z', 'values': ['18850.0', '748266829.167562703036783836603937695508484', '49596.0']}]}}
    print('TEST RESULT', result)
    assert dummy_result == result

def test_get_coinmetrics_network_data():
    testObj = d.Data()
    result = testObj.get_coinmetrics_network_data(api_key='mlR99PGlp1PpNiMYxcG0', asset='eth', metrics='AdrActCnt,CapRealUSD,TxCnt', start='2017-01-01', end='2017-01-05')
    dummy_result = pd.DataFrame([['2017-01-01T00:00:00.000Z', '13946.0', '734673672.319139817831833516177060007323674', '38730.0'], ['2017-01-02T00:00:00.000Z', '15232.0', '736035521.072371336253635824094185064179384', '39652.0'], ['2017-01-03T00:00:00.000Z', '14868.0', '741146428.959793620825964110400677939075684', '45883.0'], ['2017-01-04T00:00:00.000Z', '18066.0', '749721286.811463913996829494293959461077514', '50673.0'], ['2017-01-05T00:00:00.000Z', '18850.0', '748266829.167562703036783836603937695508484', '49596.0']], columns=['time', 'AdrActCnt', 'CapRealUSD', 'TxCnt'])
    print('TEST RESULT', result)
    assert dummy_result.equals(result)

def test_convert_coinmetrics_JSON_response_to_df():
    testObj = d.Data()
    test_params = {
        'metrics': 'AdrActCnt,CapRealUSD,TxCnt',
        'start': '2017-01-01',
        'end': '2017-01-05'
    }
    res = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/assets/eth/metricdata', params = test_params)
    result = testObj.convert_coinmetrics_network_data_JSON_to_df(res)
    dummy_result = pd.DataFrame([['2017-01-01T00:00:00.000Z', '13946.0', '734673672.319139817831833516177060007323674', '38730.0'], ['2017-01-02T00:00:00.000Z', '15232.0', '736035521.072371336253635824094185064179384', '39652.0'], ['2017-01-03T00:00:00.000Z', '14868.0', '741146428.959793620825964110400677939075684', '45883.0'], ['2017-01-04T00:00:00.000Z', '18066.0', '749721286.811463913996829494293959461077514', '50673.0'], ['2017-01-05T00:00:00.000Z', '18850.0', '748266829.167562703036783836603937695508484', '49596.0']], columns=['time', 'AdrActCnt', 'CapRealUSD', 'TxCnt'])
    print('TEST RESULT', result)
    assert dummy_result.equals(result)

def test_call_coinmetrics_api_trades_endpoint():
    testObj = d.Data()
    test_params = {
        'reference_time': '2019-01-01',
        'limit': 10
    }
    result = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/markets/coinbase-btc-usd-spot/trades', params = test_params)
    dummy_result = {
        "tradesData": [
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003012",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.00215325",
                "price": "3691.87",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003013",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.0015",
                "price": "3692.02",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003014",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.01",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003015",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.01",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003016",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.03",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:03.247000Z",
                "timeMicros": 1546300803247000,
                "coinMetricsId": "57003017",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.01118931",
                "price": "3692.33",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:05.267000Z",
                "timeMicros": 1546300805267000,
                "coinMetricsId": "57003018",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.01",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:05.267000Z",
                "timeMicros": 1546300805267000,
                "coinMetricsId": "57003019",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.02707147",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:05.645000Z",
                "timeMicros": 1546300805645000,
                "coinMetricsId": "57003020",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.0261652",
                "price": "3692.31",
                "side": "buy"
            },
            {
                "time": "2019-01-01T00:00:06.445000Z",
                "timeMicros": 1546300806445000,
                "coinMetricsId": "57003021",
                "marketId": "coinbase-btc-usd-spot",
                "amount": "0.00755476",
                "price": "3692.31",
                "side": "buy"
            }
        ]
    }
    print('TEST RESULT', result)
    assert dummy_result == result



def test_get_coinmetrics_trades_data():
    testObj = d.Data()
    test_params = {
        'reference_time': '2019-01-01',
        'limit': 10
    }
    result = testObj.get_coinmetrics_trades_data(api_key='mlR99PGlp1PpNiMYxcG0', market_id='coinbase-btc-usd-spot', reference_time='2019-01-01', limit= 10)
    dummy_response = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/markets/coinbase-btc-usd-spot/trades', params = test_params)
    column_headers = dummy_response['tradesData'][0].keys()
    dummy_result = pd.DataFrame(dummy_response['tradesData'], columns=column_headers)
    print('TEST RESULT', result)
    assert dummy_result.equals(result)






    