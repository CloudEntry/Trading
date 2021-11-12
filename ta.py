import pandas
import matplotlib.pyplot as plt

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

print(df.loc[df['long_conditions_met']])
df[['close', '15min50ema', '1hr50ema']].plot()
df[['macd', 'signal', 'histogram']].plot()
plt.show()

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
