import matplotlib.backends.backend_tkagg as bt
import matplotlib.pyplot as plt
import mplfinance as mpf
import tkinter as tk


class GUI(tk.Tk):
    app_name = 'Trading terminal'
    app_width = 1600
    app_height = 850
    chart_length = 141
    chart_type = 'candle'
    chart_style = mpf.make_mpf_style(
        marketcolors=mpf.make_marketcolors(
            up='#35a79b', down='#EF3434', inherit=True
        ),
        facecolor='#ffffff',
        edgecolor='#000000',
        figcolor='#ffffff', 
        gridcolor='#EEEDED',
        gridstyle='-',
        gridaxis='both',
        y_on_right=True
    )
    chart_ylabel = ''
    chart_scale = dict(left=0.15, right=0.70, top=0.44, bottom=0.65)

    def __init__(self, exchanges, strategies):
        super().__init__()

        self.strategy = None
        self.exchange = 'Binance'
        self.symbol = 'BTC/USDT'
        self.timeframe = '1d'
        self.exchanges = exchanges
        self.strategies = strategies

        self.title(GUI.app_name)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2 ) - (GUI.app_width / 2))
        y = int((screen_height / 2 ) - (GUI.app_height / 2))
        self.geometry(
            '{}x{}+{}+{}'.format(GUI.app_width, GUI.app_height, x, y)
        )

        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        symbol_menu = tk.Menu(main_menu, tearoff=0)
        binance_symbol = tk.Menu(symbol_menu, tearoff=0)
        binance_btc = tk.Menu(binance_symbol, tearoff=0)
        binance_btc.add_command(
            label='BTC/USDT', 
            command=lambda: self.set_symbol('Binance', 'BTC/USDT')
        )
        binance_btc.add_command(
            label='BTC/BUSD', 
            command=lambda: self.set_symbol('Binance', 'BTC/BUSD')
        )
        binance_symbol.add_cascade(label='BTC', menu=binance_btc)
        binance_eth = tk.Menu(binance_symbol, tearoff=0)
        binance_eth.add_command(
            label='ETH/USDT', 
            command=lambda: self.set_symbol('Binance', 'ETH/USDT')
        )
        binance_eth.add_command(
            label='ETH/BUSD', 
            command=lambda: self.set_symbol('Binance', 'ETH/BUSD')
        )
        binance_symbol.add_cascade(label='ETH', menu=binance_eth)
        symbol_menu.add_cascade(label='Binance', menu=binance_symbol)
        bitmex_symbol = tk.Menu(symbol_menu, tearoff=0)
        bitmex_xbt = tk.Menu(bitmex_symbol, tearoff=0)
        bitmex_xbt.add_command(
            label='XBTUSD', 
            command=lambda: self.set_symbol('BitMEX', 'XBTUSD')
        )
        bitmex_xbt.add_command(
            label='XBTUSDT', 
            command=lambda: self.set_symbol('BitMEX', 'XBTUSDT')
        )
        bitmex_symbol.add_cascade(label='XBT', menu=bitmex_xbt)
        bitmex_eth = tk.Menu(bitmex_symbol, tearoff=0)
        bitmex_eth.add_command(
            label='ETHUSD', 
            command=lambda: self.set_symbol('BitMEX', 'ETHUSD')
        )
        bitmex_eth.add_command(
            label='ETHUSDT', 
            command=lambda: self.set_symbol('BitMEX', 'ETHUSDT')
        )
        bitmex_symbol.add_cascade(label='ETH', menu=bitmex_eth)
        symbol_menu.add_cascade(label='BitMEX', menu=bitmex_symbol)
        main_menu.add_cascade(label='Symbol', menu=symbol_menu)
        timeframe_menu = tk.Menu(main_menu, tearoff=0)
        timeframe_menu.add_command(
            label='1 minute', 
            command=lambda: self.set_timeframe('1m')
        )
        timeframe_menu.add_command(
            label='5 minutes', 
            command=lambda: self.set_timeframe('5m')
        )
        timeframe_menu.add_command(
            label='1 hour', 
            command=lambda: self.set_timeframe('1h')
        )
        timeframe_menu.add_command(
            label='1 day', 
            command=lambda: self.set_timeframe('1d')
        )
        main_menu.add_cascade(label='Timeframe', menu=timeframe_menu)
        strategy_menu = tk.Menu(main_menu, tearoff=0)
        strategy_menu.add_command(
            label='Delete strategy',
            command=lambda: self.set_strategy(
                self.exchange, self.symbol, self.timeframe, None
            )
        )
        strategy_menu.add_separator()
        strategy_menu.add_command(
            label='Strategy_Binance_ETHUSDT_1m',
            command=lambda: self.set_strategy(
                'Binance', 'ETH/USDT', '1m',
                'Strategy_Binance_ETHUSDT_1m'
            )
        )
        strategy_menu.add_command(
            label='Strategy_BitMEX_XBTUSD_1m',
            command=lambda: self.set_strategy(
                'BitMEX', 'XBTUSD', '1m',
                'Strategy_BitMEX_XBTUSD_1m'
            )
        )
        main_menu.add_cascade(label='Strategy', menu=strategy_menu)
        
        self.output_window = tk.Text(self, bd=1, width=30)
        self.output_window.pack(side=tk.RIGHT, fill=tk.Y)

        self.exchanges[self.exchange].set_initial_data(
            self.timeframe, self.symbol
        )
        figure, self.axes = mpf.plot(
            self.exchanges[self.exchange]. \
                data.tail(GUI.chart_length),
            type=GUI.chart_type,
            style=GUI.chart_style,
            ylabel=GUI.chart_ylabel,
            returnfig=True,
            scale_padding=GUI.chart_scale
        )
        title = self.exchange + ' • ' + \
            self.symbol + ' • ' + self.timeframe
        self.axes[0].set_title(
            label=title, fontsize=15, style='normal', loc='left'
        )
        canvas = bt.FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tool_bar = bt.NavigationToolbar2Tk(canvas, self).update()

        self.update_chart()

    def update_chart(self):
        if self.exchanges[self.exchange]. \
                update_data(self.timeframe, self.symbol):
            title = self.exchange + ' • ' + \
                self.symbol + ' • ' + self.timeframe
            if self.strategy is None:
                self.axes[0].clear()
                mpf.plot(
                    self.exchanges[self.exchange]. \
                        data.tail(GUI.chart_length),
                    type=GUI.chart_type,
                    style=GUI.chart_style,
                    ylabel='',
                    ax=self.axes[0]
                )
            else:
                self.strategies[self.strategy].calculate_strategy(
                    self.exchanges[self.exchange].data
                )
                addplot = self.strategies[self.strategy].get_addplot(
                    GUI.chart_length, self.axes[0]
                )
                deal_info = self.strategies[self.strategy].trade(
                    self.exchanges[self.exchange], self.symbol
                )
                if deal_info is not None:
                    self.output_window.insert(
                        index=tk.END, chars=deal_info
                    )
                title += ' • ' + \
                    self.strategy[:self.strategy.find('_')]
                self.axes[0].clear()
                mpf.plot(
                    self.exchanges[self.exchange]. \
                        data.tail(GUI.chart_length),
                    type=GUI.chart_type,
                    style=GUI.chart_style,
                    ylabel='',
                    addplot=addplot,
                    ax=self.axes[0]
                )
            self.axes[0].set_title(
                label=title, fontsize=15, style='normal', loc='left'
            )
            plt.draw()
        self.after(ms=5000, func=self.update_chart)

    def set_symbol(self, exchange, symbol):
        if self.exchange != exchange:
            self.strategy = None
        self.exchange = exchange
        self.symbol = symbol
        self.draw_chart()

    def set_timeframe(self, timeframe):
        self.timeframe = timeframe
        self.draw_chart()

    def set_strategy(self, exchange, symbol, timeframe, strategy):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy = strategy
        self.draw_chart()

    def draw_chart(self):
        self.exchanges[self.exchange].set_initial_data(
            self.timeframe, self.symbol
        )
        title = self.exchange + ' • ' + \
            self.symbol + ' • ' + self.timeframe
        if self.strategy is None:
            self.axes[0].clear()
            mpf.plot(
                self.exchanges[self.exchange]. \
                    data.tail(GUI.chart_length),
                type=GUI.chart_type, style=GUI.chart_style,
                ylabel='', ax=self.axes[0]
            )
        else:
            self.strategies[self.strategy].calculate_strategy(
                self.exchanges[self.exchange].data
            )
            addplot = self.strategies[self.strategy].get_addplot(
                GUI.chart_length, self.axes[0]
            )
            title += ' • ' + self.strategy[:self.strategy.find('_')]
            self.axes[0].clear()
            mpf.plot(
                self.exchanges[self.exchange]. \
                    data.tail(GUI.chart_length),
                type=GUI.chart_type, style=GUI.chart_style,
                ylabel='', addplot=addplot, ax=self.axes[0]
            )
        self.axes[0].set_title(
            label=title, fontsize=15, style='normal', loc='left'
        )
        plt.draw()