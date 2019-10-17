import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules import CryptoFrame as cf

def test_init_cryptoframe():
    testObj = cf.CryptoFrame()
    assert isinstance(testObj.cf, pd.DataFrame)


def test_transform_dates_to_yyyy_mm_dd():
    dummy_df = pd.DataFrame()
    testObj = cf.CryptoFrame()
    result = testObj.transform_dates_to_yyyy_mm_dd()
    assert dummy_df.equals(result)