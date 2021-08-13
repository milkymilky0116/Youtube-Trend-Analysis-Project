import numpy as np
from numpy.lib.arraysetops import isin
import pandas as pd
from sqlalchemy import create_engine
from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness,simple
import pymysql

tmp=[1,2]

print(isinstance(tmp,list))