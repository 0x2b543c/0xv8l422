import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules import CryptoFrame as cf
from modules import CM_API as cm

def test_init_cryptoframe():
    testObj = cf.CryptoFrame()
    result = testObj.get_data()
    assert isinstance(result, pd.DataFrame)

def test_transform_dates_to_yyyy_mm_dd():
    testObj = cf.CryptoFrame()
    column_headers = ['time', 'blockHash', 'parentBlockHash', 'height', 'AdrActRecCnt', 'AdrActCnt']
    flattened_dummy_data = [
        ['2019-01-01', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '98047f3c136976b28cff7aad4b7eece44dc6dcfca87e759bb3e4af9845b52c29', '6988615', '21.0', '40.0'], ['2019-01-01', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '6988616', '97.0', '248.0'], ['2019-01-01', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '6988617', '120.0', '373.0'], ['2019-01-01', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', '6988618', '113.0', '336.0'], ['2019-01-01', '127d451f3852a57381edeb1ba091ca398f03af5aac3703f6b08bcbeb752ac2a1', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '6988619', '51.0', '214.0']
    ]
    dummy_result = pd.DataFrame(flattened_dummy_data, columns=column_headers)

    test_data = [
        ['2019-01-01T00:00:01.000000Z', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '98047f3c136976b28cff7aad4b7eece44dc6dcfca87e759bb3e4af9845b52c29', '6988615', '21.0', '40.0'], ['2019-01-01T00:00:08.000000Z', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '23c35b3de79f597e21d90f8ace41f5ad8044f56dfd69af333c782964a9581213', '6988616', '97.0', '248.0'], ['2019-01-01T00:00:30.000000Z', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', 'f656490fa79bb867adc6a00aee6090000b8574102365b05df6751d5c1d5798ef', '6988617', '120.0', '373.0'], ['2019-01-01T00:01:09.000000Z', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '4db66f9cb7a30ed7a098a8ddd6d7a005e4e833919a6c7688a8eab3a142c7b79d', '6988618', '113.0', '336.0'], ['2019-01-01T00:01:13.000000Z', '127d451f3852a57381edeb1ba091ca398f03af5aac3703f6b08bcbeb752ac2a1', '4e48d317fcb04f9ed220b067846d80faf3047d955f06f7d9f4fab4a214934c28', '6988619', '51.0', '214.0']
    ]
    test_df = pd.DataFrame(test_data, columns=column_headers)
    testObj.load_data(test_df)
    testObj.transform_dates_to_yyyy_mm_dd()
    result = testObj.get_data()
    assert dummy_result.equals(result)