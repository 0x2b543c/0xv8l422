import pytest
import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules import Pipeline as pl
from modules import CM_API as cm

@pytest.mark.curtest
def test_init_pipeline():
    testObj = pl.Pipeline()
    result = testObj.get_data()
    assert isinstance(result, pd.DataFrame)
