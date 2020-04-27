import json
import requests
import datetime
import yaml

def send_to_api(data):
    r = requests.post(url = 'http://192.168.2.199:8041/api/fi', data = data)
    return r.text

def get_quote_data(symbol='msft', data_range='1d', data_interval='10m'):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    timelist = data['chart']['result'][0]['timestamp']
    closelist = data['chart']['result'][0]['indicators']['quote'][0]['close']
    volumelist = data['chart']['result'][0]['indicators']['quote'][0]['volume']
    stockdata = {}
    datalist = []
    for f, b, g in zip(timelist,closelist,volumelist):
        tmpdict = {
             'stock_date': "{0}".format(datetime.datetime.fromtimestamp(f)),
             'price': b,
             'volume': g,
             'ticker': symbol
        }
        json_data = json.dumps(tmpdict)        
        output = send_to_api(json_data)
        return output 

if __name__ == "__main__":
   with open('stocks_collect.yml') as file:
       conf = yaml.load(file)

   for ticker in conf['tickers']:
       get_quote_data(ticker, '1d', '1m')
