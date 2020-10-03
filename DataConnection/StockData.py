from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from datetime import datetime
import pandas as pd
import os

os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
os.environ['IEX_TOKEN'] = 'Tsk_b7a45cc65e624a55a5688d15eac1b692'


class StockDataFrame:
    ticker = 'n/a'
    startDate = datetime(1980, 1, 1)
    endDate = datetime(1980, 1, 1)
    datatype = 'n/a'
    data = pd.DataFrame()

    def __init__(self, symbol):
        self.ticker = symbol

    def get_historical(self, start, end, output_format='DataFrame'):
        self.datatype = 'historical'
        self.startDate = start
        self.endDate = end
        self.data = pd.DataFrame.from_dict(get_historical_data(self.ticker, start, end), orient='index',columns=['open','high','low','close','volume'])
        self.data.index.name = "Date"
        self.data = self.data.reset_index()
        self.data.index.name = "Entry_Id"


