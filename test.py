import time
import MetaTrader5 as mt5
from datetime import datetime
from candle import Candle
from conditions import candlestick_type
import sys
import pandas as pd


def take_trend(rates, period) -> bool:
    # Create a DataFrame from the historical data
    df = pd.DataFrame(rates)
    # Convert seconds to DateTime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['MA'] = df['close'].rolling(window=period).mean()

    # Determine the trend
    if df['close'].iloc[-1] > df['MA'].iloc[-1]:
        return True
    elif df['close'].iloc[-1] < df['MA'].iloc[-1]:
        return False


server = "RoboForex-ECN"
password = "m1234567"
login = 67079899
symbol: str = "XAUUSD"
timeframe = mt5.TIMEFRAME_M1
ma_period: int = 20

if not mt5.initialize(login=login, server=server):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

authorized = mt5.login(login, password, server)

if authorized:
    print("Starting...")
    while True:
        try:
            datetime_utc = datetime.fromtimestamp(mt5.symbol_info(symbol)[10])
            point = mt5.symbol_info(symbol).point

            minute = int(datetime.strftime(datetime_utc, "%M"))
            second = int(datetime.strftime(datetime_utc, "%S"))

            if second == 1:
                data = mt5.copy_rates_from_pos(
                    symbol,
                    timeframe,
                    0,
                    23
                )

                # defining four candles
                first_candle = data[-4]
                second_candle = data[-3]
                third_candle = data[-2]
                current_candle = data[-1]

                candle3 = Candle(third_candle['high'], third_candle['low'], third_candle['open'], third_candle['close'])
                candle2 = Candle(second_candle['high'], second_candle['low'], second_candle['open'], second_candle['close'])
                candle1 = Candle(first_candle['high'], first_candle['low'], first_candle['open'], first_candle['close'])

                # First and third candle should be green
                candle1_color = candle1.is_green_or_red()
                candle2_color = candle2.is_green_or_red()
                candle3_color = candle3.is_green_or_red()

                # Trend of 100 candles before second candle
                trend = take_trend(data[:20], ma_period)

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

                if candle2_type and (candle2.body() < candle1.body()):
                    if candle2_type in ['Shooting Star', 'Hanging Man']:
                        price = mt5.symbol_info_tick(symbol).bid
                        sl = second_candle['high']
                        type_of_order = mt5.ORDER_TYPE_SELL
                        tp = price - candle2.length()
                    else:
                        price = mt5.symbol_info_tick(symbol).ask
                        type_of_order = mt5.ORDER_TYPE_BUY
                        sl = second_candle['low']
                        tp = price + candle2.length()

                    reward: float = abs(tp - price)
                    risk: float = abs(price - sl)
                    current_avg = reward / risk

                    print(f"- - - - - {candle2_type} - - - - -")

                    if current_avg > 2:
                        request = {
                            'action': mt5.TRADE_ACTION_DEAL,
                            'symbol': symbol,
                            'volume': 0.01,
                            'type': type_of_order,
                            'price': price,
                            "sl": sl, 'tp': tp, 'type_time': mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_FOK
                        }
                        order = mt5.order_send(request)
                        print(f"current average : {current_avg:.2f}")

                print(f"Time -> {datetime.utcfromtimestamp(current_candle['time'])}\n"
                      f"1. Trend -> {trend}\n"
                      f"2. First Candle Color -> {candle1_color}\n"
                      f"3. Third Candle Color -> {candle3_color}\n"
                      )
                time.sleep(30)

        except KeyboardInterrupt:
            mt5.shutdown()
            sys.exit()
