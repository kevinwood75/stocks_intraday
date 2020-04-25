import json
import requests
import datetime
import pymongo
import yaml
mongo_client = pymongo.MongoClient('192.168.2.148', 27017)
mongo_db = mongo_client['woodez-fi']
collection_name = 'market_data'
db_cm = mongo_db[collection_name]


def insert_mongo(data):
    db_cm.insert(data)

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
             "date": datetime.datetime.fromtimestamp(f),
             "price": b,
             "volume": g,
             "ticker": symbol
        }
        
        insert_mongo(tmpdict)
      

if __name__ == "__main__":
   with open('stocks_collect.yml') as file:
       conf = yaml.load(file)

#   stocks = ['SQ','MSFT','TWLO','SPLK','FB','SNAP','NPI.TO','BYL.TO','NOK','TSLA','GILD']
   for ticker in conf['tickers']:
       get_quote_data(ticker, '5d', '1m')
#   cursor = db_cm.find({})
#   for document in cursor:
#       print(document)
