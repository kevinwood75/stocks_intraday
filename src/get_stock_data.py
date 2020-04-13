import requests
import pandas as pd
import arrow
from dateutil.parser import parse
from dateutil.tz import gettz
import datetime
from pprint import pprint
import urllib,time,datetime
import sys

symbol1 = sys.argv[1]
symbolname = symbol1
symbol1 = symbol1.upper()

def get_quote_data(symbol='msft', data_range='1d', data_interval='10m'):
     res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
     data = res.json()
     body = data['chart']['result'][0]
     dt = datetime.datetime
     dt = pd.Series(map(lambda x: arrow.get(x).to('EST').datetime.replace(tzinfo=None), body['timestamp']), name='dt')
     df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
     dg = pd.DataFrame(body['timestamp'])
     return df.loc[:, ('open', 'high', 'low', 'close', 'volume')]

q = get_quote_data(symbol1, '1d', '1m')
print(q.head())
#print(q['close'].mean())

