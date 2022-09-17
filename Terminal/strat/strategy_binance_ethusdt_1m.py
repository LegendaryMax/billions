import matplotlib.markers as mark
import mplfinance as mpf
import pandas_ta as ta
import pandas as pd


class Strategy_Binance_ETHUSDT_1m():
    long = False
    ema_fast_length = 5
    ema_slow_length = 15
    ema_fast_color = '#483D8B'
    ema_slow_color = '#FFA500'
    long_marker_color = '#1c68fa'
    exit_marker_color = '#cf11f4'
    long_marker = mark.CARETRIGHT
    exit_marker = mark.CARETLEFT
    marker_size = 50
    trade_start = False
    qty_percent = 50

    def calculate_strategy(self, data):
        self.long_signals = pd.Series(
            [None] * data.shape[0]
        ).astype(float)
        self.exit_signals = pd.Series(
            [None] * data.shape[0]
        ).astype(float)
        self.ema_fast = ta.ema(data['close'], self.ema_fast_length)
        self.ema_slow = ta.ema(data['close'], self.ema_slow_length)
        self.cross_up = ta.crossover(self.ema_fast, self.ema_slow)
        self.cross_down = ta.crossunder(self.ema_fast, self.ema_slow)

        for i in range(data.shape[0]):
            if self.cross_down[i] and self.long:
                self.long = False
                self.exit_signals[i] = data['close'][i]
            elif self.cross_up[i] and not self.long:
                self.long = True
                self.long_signals[i] = data['close'][i] 

    def get_addplot(self, chart_length, axes):
        addplot = [
            mpf.make_addplot(
                self.ema_fast.tail(chart_length),
                color=self.ema_fast_color,
                ax=axes
            ),
            mpf.make_addplot(
                self.ema_slow.tail(chart_length),
                color=self.ema_slow_color,
                ax=axes
            ),
            mpf.make_addplot(
                self.long_signals.tail(chart_length),
                type='scatter',
                marker=self.long_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes
            ),
            mpf.make_addplot(
                self.exit_signals.tail(chart_length),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.exit_marker_color,
                ax=axes
            )
        ]
        return addplot

    def trade(self, exchange, symbol):
        if self.trade_start:
            if not pd.isna(self.exit_signals.iloc[-1]):
                return exchange.order_market_sell(symbol, 100)

        if not pd.isna(self.long_signals.iloc[-1]):
            self.trade_start = True
            return exchange.order_market_buy(symbol, self.qty_percent)