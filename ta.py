import pandas
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_candlestick(dfpl):
    fig = make_subplots(rows=2, cols=1)
    fig.append_trace(go.Candlestick(x=dfpl.index,
                                    open=dfpl['open'],
                                    high=dfpl['high'],
                                    low=dfpl['low'],
                                    close=dfpl['close']), row=1, col=1)
    fig.add_scatter(x=dfpl.index, y=dfpl['point_pos'], mode="markers",
                    marker=dict(size=10, color="MediumPurple"),
                    name="pivot", row=1, col=1)
    fig.append_trace(go.Scatter(x=dfpl.index, y=dfpl['macd'], name='macd'), row=2, col=1)
    fig.append_trace(go.Scatter(x=dfpl.index, y=dfpl['signal'], name='signal'), row=2, col=1)
    fig.add_trace(go.Bar(x=dfpl.index, y=df['histogram'], name='histogram'), row=2, col=1)
    fig.add_scatter(x=dfpl.index, y=dfpl['macd_point_pos'], mode="markers",
                    marker=dict(size=10, color="MediumPurple"),
                    name="pivot", row=2, col=1)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


def pivot_id(df1, l, n1, n2):  # n1 n2 before and after candle l
    if l - n1 < 0 or l + n2 >= len(df1):
        return 0

    piv_id_low = 1
    piv_id_high = 1
    for i in range(l - n1, l + n2 + 1):
        if df1.low[l] > df1.low[i]:
            piv_id_low = 0
        if df1.high[l] < df1.high[i]:
            piv_id_high = 0
    if piv_id_low and piv_id_high:
        return 3
    elif piv_id_low:
        return 1
    elif piv_id_high:
        return 2
    else:
        return 0


def macd_pivot_id(df1, l, n1, n2):  # n1 n2 before and after candle l
    if l - n1 < 0 or l + n2 >= len(df1):
        return 0

    piv_id_low = 1
    piv_id_high = 1
    for i in range(l - n1, l + n2 + 1):
        if df1.macd[l] > df1.macd[i]:
            piv_id_low = 0
        if df1.macd[l] < df1.macd[i]:
            piv_id_high = 0
    if piv_id_low and piv_id_high:
        return 3
    elif piv_id_low:
        return 1
    elif piv_id_high:
        return 2
    else:
        return 0


def point_pos(x):
    if x['pivot'] == 1:
        return x['low']-1e-3
    elif x['pivot'] == 2:
        return x['high']+1e-3
    else:
        return np.nan


def macd_point_pos(x):
    if x['macd_pivot'] == 1:
        return x['macd']-1e-3
    elif x['macd_pivot'] == 2:
        return x['macd']+1e-3
    else:
        return np.nan


'''
long:
1. 15min50ema is over 1hr50ema
2. macd and signal below zero
3. lower low on price action, higher low on the macd
4. makes sure macd and signal not equal to or more than zero during lows
5. hist goes negative->positive->negative between macd and signal lows
6. enter trade when macd crosses signal
      stop loss: 2 pips below nearest swing low
      target: risk/reward ratio 2
'''
df = pandas.read_csv('data/january_AAPL.csv')

df['long_conditions_met'] = (df['15min50ema'] > df['1hr50ema']) & (df['macd'] < 0) & (df['signal'] < 0)

# get maximas and minimas
df['pivot'] = df.apply(lambda x: pivot_id(df, x.name, 5, 5), axis=1)
df['macd_pivot'] = df.apply(lambda x: macd_pivot_id(df, x.name, 5, 5), axis=1)
df['point_pos'] = df.apply(lambda row: point_pos(row), axis=1)
df['macd_point_pos'] = df.apply(lambda row: macd_point_pos(row), axis=1)

pandas.set_option('display.expand_frame_repr', False)
print(df[732:742])

# plot graph
plot_candlestick(df[600:800])

'''
short:
1. 15min50ema is under 1hr50ema
2. macd and signal above zero
3. higher high on price action, lower high on macd
4. make sure macd and signal not equal to or less than zero during highs
5. hist goes positive->negative->positive between macd and signal highs
6. enter trade when macd crosses signal
      stop loss: 2 pips above nearest swing high
      target: risk/reward ratio 2
'''
