import pytest
import sys
import os 
import pandas as pd
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules.Pipelines.FlowsPipe import FlowsPipe

@pytest.mark.curtest
def test_flows_pipeline():
    api_key = 'KKzV6V2DTY87v3m1dGZu'
    exchanges = ['BMX']
    assets = ['btc']
    start = '2019-01-01'
    pipe = FlowsPipe(api_key=api_key, exchanges=exchanges, assets=assets, start=start)
    df = pipe.run_pipeline().get_data()
    print('Result', df)
