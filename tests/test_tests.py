
import sys
import os 
dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.append(dir_path)
# sys.path.append(os.path.abspath('../modules'))
# from modules.test import test_func

from modules import test as t

print(t.test_func(100))
def test_add_ten():
    assert t.test_func(12) == 22