import csv
import yfinance as yf
import pandas as pd


class YahooAPI():



    @classmethod
    def get_quotes_yf(cls, tickerStrings, timeframe='???'):
        df_list = list()
        for ticker in tickerStrings:
            data = yf.download(ticker, group_by="Ticker", period='max')
            data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
            df_list.append(data)

        # combine all dataframes into a single dataframe
        df = pd.concat(df_list)

        # save to csv
        df.to_csv(f'../quotes/{timeframe}-{tickerStrings}.csv')

    @classmethod
    def get_quotes_from_csv(cls, name):
        with open(name, errors='ignore', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file,
                                    fieldnames=['date', 'open', 'high', 'low', 'close', 'adj-close', 'volume', 'ticker'])
            data = list(reader)[1::]
            return data

