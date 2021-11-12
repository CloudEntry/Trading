from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from _datetime import datetime, timedelta, timezone
import btalib


def start():
    t = (datetime.now(timezone.utc) - timedelta(hours=8, minutes=15)).isoformat()
    # return t.replace('.' + t.split('.')[1].split('+')[0], '')
    return "2021-01-01T08:01:00Z"


def end():
    t = (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat()
    # return t.replace('.' + t.split('.')[1].split('+')[0], '')
    return "2021-02-01T16:01:00Z"


def get_data(ticker):
    api = REST()

    # get the 5 minute bars
    df = api.get_bars(ticker, TimeFrame(5, TimeFrameUnit.Minute), start(), end(), adjustment='raw').df

    # get the 1 hour 50 EMA
    df_hour = api.get_bars(ticker, TimeFrame.Hour, start(), end(), adjustment='raw').df
    df['1hr50ema'] = btalib.ema(df_hour, period=50).df
    df['1hr50ema'] = df['1hr50ema'].ffill()

    # get the 15 minute 50 EMA
    df_15_min = api.get_bars(ticker, TimeFrame(15, TimeFrameUnit.Minute), start(), end(), adjustment='raw').df
    df['15min50ema'] = btalib.ema(df_15_min, period=50).df
    df['15min50ema'] = df['15min50ema'].ffill()

    # get macd
    macd = btalib.macd(df).df
    df['macd'] = macd['macd']
    df['signal'] = macd['signal']
    df['histogram'] = macd['histogram']

    return df


data = get_data("AAPL")
data.to_csv('data/january_AAPL.csv')
