from Terminal import api

if __name__ == '__main__':
    print(api.YahooAPI.get_quotes_from_csv('1D-BTCUSDT'))