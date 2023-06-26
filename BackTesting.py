import pytz
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from candle import Candle
import pandas as pd
from conditions import candlestick_type

server = "RoboForex-ECN"
password = "m1234567"
login = 67079899
symbol: str = "XAUUSD"
counter: int = 0
tp_counter: int = 0
sl_counter: int = 0
timeframe = mt5.TIMEFRAME_M5
ma_period: int = 50
trend_to: int = ma_period


def test(rates, t, s):
    tp_hit = True
    sl_hit = False
    # Increasing trend
    for rate in rates:
        if t > s:
            if rate['high'] >= t:
                print("tp hit")
                return tp_hit
            elif rate['low'] <= s:
                print('sl hit')
                return sl_hit
        else:
            if rate['low'] <= t:
                print("tp hit")
                return tp_hit
            elif rate['high'] >= s:
                print('sl hit')
                return sl_hit


if not mt5.initialize(login=login, server=server):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

authorized = mt5.login(login, password, server)

if authorized:
    print("Starting....")

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2023, 6, 22, tzinfo=timezone)
    utc_to = datetime(2023, 6, 23, tzinfo=timezone)

    rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # df.set_index('time', inplace=True)

    # Calculate the moving average using a rolling window and the mean function
    moving_averages = df['close'].rolling(window=ma_period).mean()

    for i in range(ma_period, len(df)):
        third_candle = rates[i-1]
        second_candle = rates[i-2]
        first_candle = rates[i-3]

        candle3 = Candle(third_candle['high'], third_candle['low'], third_candle['open'], third_candle['close'])
        candle2 = Candle(second_candle['high'], second_candle['low'], second_candle['open'], second_candle['close'])
        candle1 = Candle(first_candle['high'], first_candle['low'], first_candle['open'], first_candle['close'])

        # First and third candle should be green
        candle1_color = candle1.is_green_or_red()
        candle2_color = candle2.is_green_or_red()
        candle3_color = candle3.is_green_or_red()

        # Volume for second and third candle
        candle2_volume = second_candle['tick_volume']
        candle3_volume = third_candle['tick_volume']

        current_candle = df.iloc[i]
        current_ma = moving_averages.iloc[i]

        # Determine the trend based on the current price and moving average
        if current_candle['close'] > current_ma:
            trend = True
        elif current_candle['close'] < current_ma:
            trend = False
        else:
            trend = None

        # Check second candle type
        candle2_type = candlestick_type(
            candle2.body(),
            candle2.upper_shadow(),
            candle2.lower_shadow(),
            candle1_color,
            candle3_color,
            second_candle['close'],
            third_candle['close'],
            trend,
            candle2_color,
            second_candle['open']
        )
        print(trend, datetime.strftime(datetime.fromtimestamp(second_candle['time'])-timedelta(hours=3),'%d %H,:%M'), candle2_type)
        #
        # if candle2_type:
        #     if candle2_type == 'Shooting Star' or 'Hanging Man':
        #         price = mt5.symbol_info_tick(symbol).bid
        #         sl = second_candle['high']
        #         type_of_order = mt5.ORDER_TYPE_SELL
        #         tp = price - candle2.length() * 2
        #     else:
        #         price = mt5.symbol_info_tick(symbol).ask
        #         type_of_order = mt5.ORDER_TYPE_BUY
        #         sl = second_candle['low']
        #         tp = price + candle2.length() * 2
        #
        #     request = {
        #         'action': mt5.TRADE_ACTION_DEAL,
        #         'symbol': symbol,
        #         'volume': 0.01,
        #         'type': type_of_order,
        #         'price': price,
        #         "sl": sl, 'tp': tp, 'type_time': mt5.ORDER_TIME_GTC,
        #         "type_filling": mt5.ORDER_FILLING_FOK
        #     }
        #     result = mt5.order_send(request)
        #     reward: float = abs(tp - price)
        #     risk: float = abs(price - sl)
        #
        # print(f"- - - - {candle2_type} - - - -")
        # print(f"Time -> {(datetime_utc - (datetime_utc - datetime.now())).strftime('%H:%M')}\n"
        #       f"1. Trend -> {trend}\n"
        #       f"2. First Candle Color -> {candle1_color}\n"
        #       f"3. Third Candle Color -> {candle3_color}\n"
        #       f"4. Candle2 volume < Candle3 volume -> {candle2_volume < candle3_volume}"
        #       )
