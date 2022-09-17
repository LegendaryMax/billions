import bitmex as bm
import pandas as pd
import time


class BitmexAPI():
    def __init__(self, test, api_key, api_secret):
        self.client = bm.bitmex(
            test=test, api_key=api_key, api_secret=api_secret
        )

    def set_initial_data(self, timeframe, symbol):
        while True:
            try:
                self.data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.Trade.Trade_getBucketed(
                            binSize=timeframe,
                            symbol=symbol,
                            count=1000,
                            reverse=True
                        ).result()[0]
                    )[::-1],
                    columns=[
                        'timestamp', 'open', 'high',
                        'low', 'close', 'volume'
                    ]
                ).set_index('timestamp').shift(-1)[:-1]
            except:
                time.sleep(0.5)
            else:
                break

    def update_data(self, timeframe, symbol):
        while True:
            try:
                last_data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.Trade.Trade_getBucketed(
                            binSize=timeframe,
                            symbol=symbol,
                            count=2,
                            reverse=True
                        ).result()[0]
                    )[::-1],
                    columns=[
                        'timestamp', 'open', 'high',
                        'low', 'close', 'volume'
                    ]
                ).set_index('timestamp').shift(-1)[:-1]
            except:
                time.sleep(0.5)
            else:
                break
        if last_data.index[0] != self.data.index[-1]:
            self.data = pd.concat([self.data, last_data])
            return True

    def create_market_order(self, symbol, side, qty_percent, leverage):
        try:
            self.client.Position.Position_updateLeverage(
                symbol=symbol, leverage=leverage
            ).result()
            quote = self.client.Quote.Quote_get(
                symbol=symbol, count=1, reverse=True
            ).result()[0][0]
            bid = quote['bidPrice']
            ask = quote['askPrice']
            if side == 'Buy':
                price = ask
            else:
                price = bid
            if symbol.endswith('USD'):
                available_margin = self.client.User. \
                    User_getMargin(currency='XBt'). \
                    result()[0]['availableMargin'] / 10**8
                if symbol == 'XBTUSD':
                    qty = 100 * int(
                        (available_margin * leverage * qty_percent /
                        100) / (1 / price) / 100
                    )
                    order_text = ' USD of '
                else:
                    qty = int(
                        (available_margin * leverage * qty_percent /
                        100) / 
                        (price * self.client.Instrument.Instrument_get(
                            symbol=symbol
                        ).result()[0][0]['multiplier'] / 10**8)
                    )
                    order_text = ' cont of '
                order_qty = str(qty) + order_text + symbol
            elif symbol.endswith('USDT'):  
                available_margin = self.client.User. \
                    User_getMargin(currency='USDt'). \
                    result()[0]['availableMargin'] / 10**6
                qty = 1000 * int(
                    (available_margin * leverage * qty_percent / 100) /
                    (price * (1 / 
                    self.client.Instrument.Instrument_get(
                        symbol=symbol
                    ).result()[0][0]['underlyingToPositionMultiplier'])
                    ) / 1000
                )
                order_text = ' ' + symbol[:symbol.find('USDT')] + \
                    ' of '
                order_qty = str(round(qty * \
                    (1 / self.client.Instrument.Instrument_get(
                        symbol=symbol
                    ).result()[0][0]['underlyingToPositionMultiplier']
                    ), 3)) + order_text + symbol
            order = self.client.Order.Order_new(
                symbol=symbol, side=side, orderQty=qty
            ).result()[0]
            avg_price = str(round(order['avgPx'], 8))
            t = order['transactTime'].strftime('%Y-%m-%d %H:%M')
            if side == 'Buy':
                position = 'Market buy order filled'
            else:
                position = 'Market sell order filled'
            result = position + \
                '\nQty: ' + order_qty + \
                '\nAverage price: ' + avg_price + \
                '\nTime: ' + t + '\n\n'       
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            return str(e) + '\nTime: ' + t + '\n\n'
        else:
            return result

    def close_position(self, symbol):
        try:
            qty = self.client.Position.Position_get(
            	filter='{"symbol": "%s"}' % symbol
            ).result()[0][0]['currentQty']
            if symbol.endswith('USD'):
                if qty > 0:
                    position = 'Market sell order filled'
                else:
                    position = 'Market buy order filled'
                    qty = abs(qty)
                if symbol == 'XBTUSD':
                    order_text = ' USD of '
                else:
                    order_text = ' cont of '
                order_qty = str(qty) + order_text + symbol
            elif symbol.endswith('USDT'):
                if qty > 0:
                    position = 'Market sell order filled'
                    qty *= (1 / self.client.Instrument.Instrument_get(
                        symbol=symbol
                    ).result()[0][0]['underlyingToPositionMultiplier'])
                else:
                    position = 'Market buy order filled'
                    qty *= -(1 / self.client.Instrument.Instrument_get(
                        symbol=symbol
                    ).result()[0][0]['underlyingToPositionMultiplier'])
                order_text = ' ' + \
                    symbol[:symbol.find('USDT')] + ' of '
                order_qty = str(round(qty, 3)) + order_text + symbol
            order = self.client.Order. \
                Order_closePosition(symbol=symbol).result()[0]
            avg_price = str(round(order['avgPx'], 8))
            t = order['transactTime'].strftime('%Y-%m-%d %H:%M')
            result = position + \
                '\nQty: ' + order_qty + \
                '\nAverage price: ' + avg_price + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            return str(e) + '\nTime: ' + t + '\n\n'
        else:
            return result