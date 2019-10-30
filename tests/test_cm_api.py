import pytest
import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules import CM_API as cm

def test_call_coinmetrics_api():
    testObj = cm.CM_API()
    test_params = {
        'metrics': 'AdrActCnt,CapRealUSD,TxCnt',
        'start': '2017-01-01',
        'end': '2017-01-05'
    }
    result = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/assets/eth/metricdata', params = test_params)
    dummy_result = {'metricData': {'metrics': ['AdrActCnt', 'CapRealUSD', 'TxCnt'], 'series': [{'time': '2017-01-01T00:00:00.000Z', 'values': ['13946.0', '734673672.319139817831833516177060007323674', '38730.0']}, {'time': '2017-01-02T00:00:00.000Z', 'values': ['15232.0', '736035521.072371336253635824094185064179384', '39652.0']}, {'time': '2017-01-03T00:00:00.000Z', 'values': ['14868.0', '741146428.959793620825964110400677939075684', '45883.0']}, {'time': '2017-01-04T00:00:00.000Z', 'values': ['18066.0', '749721286.811463913996829494293959461077514', '50673.0']}, {'time': '2017-01-05T00:00:00.000Z', 'values': ['18850.0', '748266829.167562703036783836603937695508484', '49596.0']}]}}
    assert dummy_result == result

def test_call_coinmetrics_api_trades_endpoint():
    testObj = cm.CM_API()
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
    assert dummy_result == result

def test_call_coinmetrics_api_candles_endpoint():
    testObj = cm.CM_API()
    test_params = {
        'reference_time': '2019-01-01',
        'limit': 10
    }
    result = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/markets/coinbase-btc-usd-spot/candles', params = test_params)
    dummy_result = {
        "candlesData": [
            {
                "time": "2019-01-01T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3692.31",
                "priceHigh": "3841.17",
                "priceLow": "3651.02",
                "priceClose": "3826.1",
                "vwap": "3711.46315827099",
                "volume": "10812.88498825",
                "duration": "1 day"
            },
            {
                "time": "2019-01-02T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3826.1",
                "priceHigh": "3916.57",
                "priceLow": "3770.07",
                "priceClose": "3890.79",
                "vwap": "3837.59284193891",
                "volume": "9982.47084577",
                "duration": "1 day"
            },
            {
                "time": "2019-01-03T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3890.8",
                "priceHigh": "3893.8",
                "priceLow": "3758.07",
                "priceClose": "3786.67",
                "vwap": "3826.01132353795",
                "volume": "9327.64708895",
                "duration": "1 day"
            },
            {
                "time": "2019-01-04T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3787.57",
                "priceHigh": "3849.0",
                "priceLow": "3730.0",
                "priceClose": "3820.82",
                "vwap": "3784.80476707302",
                "volume": "9225.1505004",
                "duration": "1 day"
            },
            {
                "time": "2019-01-05T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3820.82",
                "priceHigh": "3874.12",
                "priceLow": "3775.0",
                "priceClose": "3798.62",
                "vwap": "3833.51802737287",
                "volume": "6451.00775001",
                "duration": "1 day"
            },
            {
                "time": "2019-01-06T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3799.99",
                "priceHigh": "4088.0",
                "priceLow": "3756.01",
                "priceClose": "4040.99",
                "vwap": "3958.41384035492",
                "volume": "10057.45367318",
                "duration": "1 day"
            },
            {
                "time": "2019-01-07T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "4040.98",
                "priceHigh": "4070.0",
                "priceLow": "3968.79",
                "priceClose": "4006.01",
                "vwap": "4019.42512905279",
                "volume": "9973.66538481",
                "duration": "1 day"
            },
            {
                "time": "2019-01-08T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "4005.97",
                "priceHigh": "4114.8",
                "priceLow": "3943.36",
                "priceClose": "3993.86",
                "vwap": "4016.1668631788",
                "volume": "13959.39645383",
                "duration": "1 day"
            },
            {
                "time": "2019-01-09T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "3993.85",
                "priceHigh": "4042.2",
                "priceLow": "3962.12",
                "priceClose": "4004.12",
                "vwap": "4007.75789889434",
                "volume": "10704.12810583",
                "duration": "1 day"
            },
            {
                "time": "2019-01-10T00:00:00.000000Z",
                "marketId": "coinbase-btc-usd-spot",
                "priceOpen": "4004.13",
                "priceHigh": "4035.21",
                "priceLow": "3560.0",
                "priceClose": "3626.07",
                "vwap": "3754.74987721677",
                "volume": "21869.18380217",
                "duration": "1 day"
            }
        ]
    }
    assert dummy_result == result

def test_call_coinmetrics_realtime_network_data_endpoint():
    testObj = cm.CM_API()
    test_params = {
        'metrics': 'AdrActRecCnt,AdrActCnt',
        'reference_time': '2019-01-01',
        'limit': 5
    } 
    result = testObj.call_coinmetrics_api(api_key='ZHDJLW1WxLD8ttzW27am', url='https://api.coinmetrics.io/v3/assets/eth/realtimemetricdata', params = test_params)
    dummy_result = {
        "metricData": {
            "metrics": [
                "AdrActRecCnt",
                "AdrActCnt"
            ],
            "series": [
                {
                    "time": "2019-01-01T00:00:01.000000Z",
                    "blockHash": "23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213",
                    "parentBlockHash": "98047f3c136976b28cff7aad4b7eece44dc6dcfca87e759bb3e4af9845b52c29",
                    "height": "6988615",
                    "values": [
                        "21.0",
                        "40.0"
                    ]
                },
                {
                    "time": "2019-01-01T00:00:08.000000Z",
                    "blockHash": "f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef",
                    "parentBlockHash": "23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213",
                    "height": "6988616",
                    "values": [
                        "97.0",
                        "248.0"
                    ]
                },
                {
                    "time": "2019-01-01T00:00:30.000000Z",
                    "blockHash": "4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d",
                    "parentBlockHash": "f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef",
                    "height": "6988617",
                    "values": [
                        "120.0",
                        "373.0"
                    ]
                },
                {
                    "time": "2019-01-01T00:01:09.000000Z",
                    "blockHash": "4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28",
                    "parentBlockHash": "4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d",
                    "height": "6988618",
                    "values": [
                        "113.0",
                        "336.0"
                    ]
                },
                {
                    "time": "2019-01-01T00:01:13.000000Z",
                    "blockHash": "127d451f3852a57381edeb1ba091ca398f03af5aac3703f6b08bcbeb752ac2a1",
                    "parentBlockHash": "4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28",
                    "height": "6988619",
                    "values": [
                        "51.0",
                        "214.0"
                    ]
                }
            ]
        }
    }
    assert dummy_result == result

def test_convert_coinmetrics_network_data_JSON_to_df():
    testObj = cm.CM_API()
    test_params = {
        'metrics': 'AdrActCnt,CapRealUSD,TxCnt',
        'start': '2017-01-01',
        'end': '2017-01-05'
    }
    res = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/assets/eth/metricdata', params = test_params)
    result = testObj.convert_coinmetrics_network_data_JSON_to_df(res)
    dummy_result = pd.DataFrame([
        ['2017-01-01T00:00:00.000Z', '13946.0', '734673672.319139817831833516177060007323674', '38730.0'], ['2017-01-02T00:00:00.000Z', '15232.0', '736035521.072371336253635824094185064179384', '39652.0'], ['2017-01-03T00:00:00.000Z', '14868.0', '741146428.959793620825964110400677939075684', '45883.0'], ['2017-01-04T00:00:00.000Z', '18066.0', '749721286.811463913996829494293959461077514', '50673.0'], ['2017-01-05T00:00:00.000Z', '18850.0', '748266829.167562703036783836603937695508484', '49596.0']
        ], columns=['time', 'AdrActCnt', 'CapRealUSD', 'TxCnt'])
    assert dummy_result.equals(result)

@pytest.mark.curtest
def test_get_coinmetrics_network_data():
    testObj = cm.CM_API()
    result = testObj.get_coinmetrics_network_data(api_key='mlR99PGlp1PpNiMYxcG0', assets=['eth'], metrics='AdrActCnt,CapRealUSD,TxCnt', start='2017-01-01', end='2017-01-05')
    dummy_result = pd.DataFrame([
        ['2017-01-01T00:00:00.000Z', '13946.0', '734673672.319139817831833516177060007323674', '38730.0'], ['2017-01-02T00:00:00.000Z', '15232.0', '736035521.072371336253635824094185064179384', '39652.0'], ['2017-01-03T00:00:00.000Z', '14868.0', '741146428.959793620825964110400677939075684', '45883.0'], ['2017-01-04T00:00:00.000Z', '18066.0', '749721286.811463913996829494293959461077514', '50673.0'], ['2017-01-05T00:00:00.000Z', '18850.0', '748266829.167562703036783836603937695508484', '49596.0']
        ], columns=['time', 'AdrActCnt', 'CapRealUSD', 'TxCnt'])
    assert dummy_result.equals(result)

def test_get_coinmetrics_trades_data():
    testObj = cm.CM_API()
    test_params = {
        'reference_time': '2019-01-01',
        'limit': 10
    }
    result = testObj.get_coinmetrics_trades_data(api_key='mlR99PGlp1PpNiMYxcG0', market_id='coinbase-btc-usd-spot', reference_time='2019-01-01', limit= 10)
    dummy_response = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/markets/coinbase-btc-usd-spot/trades', params = test_params)
    column_headers = dummy_response['tradesData'][0].keys()
    dummy_result = pd.DataFrame(dummy_response['tradesData'], columns=column_headers)
    assert dummy_result.equals(result)

def test_get_coinmetrics_candles_data():
    testObj = cm.CM_API()
    test_params = {
        'reference_time': '2019-01-01',
        'limit': 10
    }
    result = testObj.get_coinmetrics_candles_data(api_key='mlR99PGlp1PpNiMYxcG0', market_id='coinbase-btc-usd-spot', reference_time='2019-01-01', limit= 10)
    dummy_response = testObj.call_coinmetrics_api(api_key='mlR99PGlp1PpNiMYxcG0', url='https://api.coinmetrics.io/v3/markets/coinbase-btc-usd-spot/candles', params = test_params)
    column_headers = dummy_response['candlesData'][0].keys()
    dummy_result = pd.DataFrame(dummy_response['candlesData'], columns=column_headers)
    assert dummy_result.equals(result)

def test_get_realtime_network_data():
    testObj = cm.CM_API()
    test_params = {
        'metrics': 'AdrActRecCnt,AdrActCnt',
        'reference_time': '2019-01-01',
        'limit': 5
    } 
    dummy_response = testObj.call_coinmetrics_api(api_key='ZHDJLW1WxLD8ttzW27am', url='https://api.coinmetrics.io/v3/assets/eth/realtimemetricdata', params = test_params)
    column_headers = list(dummy_response['metricData']['series'][0].keys())[:-1] + dummy_response['metricData']['metrics']
    
    flattened_dummy_data = [
        ['2019-01-01T00:00:01.000000Z', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '98047f3c136976b28cff7aad4b7eece44dc6dcfca87e759bb3e4af9845b52c29', '6988615', '21.0', '40.0'], ['2019-01-01T00:00:08.000000Z', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '6988616', '97.0', '248.0'], ['2019-01-01T00:00:30.000000Z', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '6988617', '120.0', '373.0'], ['2019-01-01T00:01:09.000000Z', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', '6988618', '113.0', '336.0'], ['2019-01-01T00:01:13.000000Z', '127d451f3852a57381edeb1ba091ca398f03af5aac3703f6b08bcbeb752ac2a1', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '6988619', '51.0', '214.0']
    ]
    dummy_result = pd.DataFrame(flattened_dummy_data, columns=column_headers)

    result = testObj.get_coinmetrics_realtime_network_data(api_key='ZHDJLW1WxLD8ttzW27am', asset_id='eth', metrics='AdrActRecCnt,AdrActCnt', reference_time='2019-01-01', limit= 5)
    assert dummy_result.equals(result)






    