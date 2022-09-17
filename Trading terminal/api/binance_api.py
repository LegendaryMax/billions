import binance as bn
import pandas as pd
import time


class BinanceAPI():
    def __init__(self, test, api_key, api_secret):
        self.client = bn.Client(
            testnet=test, api_key=api_key, api_secret=api_secret
        )

    def set_initial_data(self, timeframe, symbol):
        while True:
            try:
                self.data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.get_klines(
                            symbol=symbol.replace('/', ''),
                            interval=timeframe,
                            limit=1000
                        ),
                        columns=[
                            'timestamp', 'open', 'high', 'low',
                            'close', 'volume', 'close time',
                            'quote asset volume','number of trades',
                            'taker buy base asset volume',
                            'taker buy quote asset volume',
                            'can be ignored'
                        ]
                    )[:-1],
                    columns=[
                        'timestamp', 'open', 'high',
                        'low', 'close', 'volume'
                    ]
                ).set_index('timestamp').astype(float)
                self.data.index = pd.to_datetime(
                    self.data.index, unit='ms', utc=True
                )
            except:
                time.sleep(0.5)
            else:
                break

    def update_data(self, timeframe, symbol):
        while True:
            try:
                last_data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.get_klines(
                            symbol=symbol.replace('/', ''),
                            interval=timeframe,
                            limit=2
                        ),
                        columns=[
                            'timestamp', 'open', 'high', 'low',
                            'close', 'volume', 'close time',
                            'quote asset volume','number of trades', 
                            'taker buy base asset volume',
                            'taker buy quote asset volume',
                            'can be ignored'
                        ]
                    )[:-1],
                    columns=[
                        'timestamp', 'open', 'high',
                        'low', 'close', 'volume'
                    ]
                ).set_index('timestamp').astype(float)
                last_data.index = pd.to_datetime(
                    last_data.index, unit='ms', utc=True
                )
            except:
                time.sleep(0.5)
            else:
                break
        if last_data.index[-1] != self.data.index[-1]:
            self.data = pd.concat([self.data, last_data])
            return True

    def order_market_buy(self, symbol, qty_percent):
        try:
            quote = self.client.get_orderbook_ticker(
                symbol=symbol.replace('/', '')
            )
            price = float(quote['askPrice'])
            currency = float(self.client.get_asset_balance(
                asset=symbol[symbol.find('/') + 1:]
            )['free'])
            qty = currency * qty_percent / 100 / price
            lot_size = float(self.client.get_symbol_info(
                symbol.replace('/', '')
            )['filters'][2]['minQty'])
            qty =  round(int(qty / lot_size) * lot_size, 8)
            order = self.client.order_market_buy(
                symbol=symbol.replace('/', ''), quantity=qty
            )
            avg_price = 0
            for i in order['fills']:
                avg_price += float(i['price']) * float(i['qty']) / qty
            order_qty = str(round(float(order['executedQty']), 5)) + \
                ' ' + symbol[:symbol.find('/')]
            avg_price = str(round(avg_price, 8))
            t = pd.to_datetime(
                order['transactTime'], unit='ms', utc=True
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Market buy order filled' + \
                '\nQty: ' + order_qty + \
                '\nAverage price: ' + avg_price + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            return str(e) + '\nTime: ' + t + '\n\n'
        else:
            return result

    def order_market_sell(self, symbol, qty_percent):
        try:
            asset = float(self.client.get_asset_balance(
                asset=symbol[:symbol.find('/')]
            )['free'])
            qty = asset * qty_percent / 100
            lot_size = float(self.client.get_symbol_info(
                symbol.replace('/', '')
            )['filters'][2]['minQty'])
            qty =  round(int(qty / lot_size) * lot_size, 8)
            order = self.client.order_market_sell(
                symbol=symbol.replace('/', ''), quantity=qty
            )
            avg_price = 0
            for i in order['fills']:
                avg_price += float(i['price']) * float(i['qty']) / qty
            order_qty = str(round(float(order['executedQty']), 5)) + \
                ' ' + symbol[:symbol.find('/')]
            avg_price = str(round(avg_price, 8))
            t = pd.to_datetime(
                order['transactTime'], unit='ms', utc=True
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Market sell order filled' + \
                '\nQty: ' + order_qty + \
                '\nAverage price: ' + avg_price + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            return str(e) + '\nTime: ' + t + '\n\n'
        else:
            return result