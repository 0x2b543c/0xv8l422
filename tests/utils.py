import os
import sys
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)

from modules.Transformers.DateNormalizer import DateNormalizer
from modules.Transformers.CastToFloats import CastToFloats

def clean_test_data(self, df):
    df = DateNormalizer().transform(df)
    df = CastToFloats().transform(df)
    return df

def log_test_data(dummy_result, result):
    print('Expected result:', dummy_result)
    print('Real result:', result)

