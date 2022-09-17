import strat
import api
import gui

exchanges = {
    'Binance': api.BinanceAPI(
        test=False,
        api_key='t5kUo9Maz2tChGCuCYrqiSjom6Af8q9z4ZUpYMn17CaNKv1uf' + \
            '6OPPXyYF6nmfiSg',
        api_secret='cLiqBmbspJJPggXcXMrR3p0vIBxGouoZVHf4LngYtcIOHh' + \
            'tP6NYu8P4jYiIlbCRE'
    ),
    'BitMEX': api.BitmexAPI(
        test=True,
        api_key='KTRji57RDHEpt-qJ7W90wKQz',
        api_secret='7wFMYt6-2I_W7g6A29etf4X6nhNAH3urpjxOn41Gd_aqMOkW'
    )
}
strategies = {
    'Strategy_Binance_ETHUSDT_1m': strat.Strategy_Binance_ETHUSDT_1m(),
    'Strategy_BitMEX_XBTUSD_1m': strat.Strategy_BitMEX_XBTUSD_1m()
}
root = gui.GUI(exchanges, strategies)
root.mainloop()