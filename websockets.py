# from alpaca_trade_api import Stream
# from alpaca_trade_api.common import URL
# from alpaca_trade_api.entity import Bar
# import datetime
# import os
#
#
# async def bar_callback(b: Bar):
#     print('close', b.close)
#     print('timestamp', datetime.timedelta(seconds=b.timestamp/1000))
#
#
# stream = Stream(os.environ['APCA_API_KEY_ID'],
#                 os.environ['APCA_API_SECRET_KEY'],
#                 base_url=URL('https://paper-api.alpaca.markets'),
#                 data_feed='iex')
#
# stream.subscribe_bars(bar_callback, 'AAPL')
# stream.run()
