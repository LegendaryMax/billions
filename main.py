from Terminal.api.yf_api import YahooAPI
import mplfinance as mpf


if __name__ == '__main__':
    # quotes from text file
    data = YahooAPI.get_quotes_from_csv('Terminal/quotes/1D-BTCUSDT.csv')
    print(data)
    # examples
    # mpf.plot(data)