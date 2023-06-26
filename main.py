import sys
import MetaTrader5 as mt5
from candle import Candle
from shoot_or_inverse import is_shooting_or_inverse
from hanging_or_hammer import is_hanging_or_hammer
import time
import pandas as pd

server = "RoboForex-ECN"
password = "m1234567"
login = 67079899

if not mt5.initialize(login=login, server=server):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

authorized = mt5.login(login, password, server)

symbol: str = "BTCUSD"
counter: int = 0

if authorized:
    print("Starting....")
    while True:
        try:
            convert_time = pd.to_datetime(mt5.symbol_info(symbol)[10], unit='s')
            time_in_s = int(f"{convert_time:%S}")
            if time_in_s == 1:

                # Get three last candles
                rates = mt5.copy_rates_from_pos(
                    symbol,
                    mt5.TIMEFRAME_M1,
                    0,
                    3
                )

                second_candle = rates[1]
                third_candle = rates[0]

                lot = 1

                candle2 = Candle(second_candle['high'], second_candle['low'], second_candle['open'],
                                 second_candle['close'])
                candle3 = Candle(third_candle['high'], third_candle['low'], third_candle['open'],
                                 third_candle['close'])

                check_shooting_or_inverse = is_shooting_or_inverse(candle3.body(),
                                                                   candle3.upper_shadow(),
                                                                   candle3.lower_shadow(),
                                                                   candle2.is_green_or_red(),
                                                                   second_candle['close'],
                                                                   third_candle['close'])

                check_hanging_or_hammer = is_hanging_or_hammer(candle3.body(),
                                                               candle3.upper_shadow(),
                                                               candle3.lower_shadow(),
                                                               candle2.is_green_or_red(),
                                                               second_candle['close'],
                                                               third_candle['close'])

                lst = [check_shooting_or_inverse, check_hanging_or_hammer]
                check_candle = all(val is None for val in lst)

                if check_candle is False:
                    print("=  =  =  =  =  =  =  =  =  =")
                    # True -> it is shooting star or hanging man
                    if check_shooting_or_inverse or check_hanging_or_hammer:
                        price = mt5.symbol_info_tick(symbol).bid
                        sl = third_candle['high']
                        type_of_order = mt5.ORDER_TYPE_SELL
                        tp = price - (sl - price)
                        if check_shooting_or_inverse:
                            print("...Shooting Star...")
                        else:
                            print("...Hanging Man...")

                    else:
                        price = mt5.symbol_info_tick(symbol).ask
                        type_of_order = mt5.ORDER_TYPE_BUY
                        sl = third_candle['low']
                        tp = price + (price - sl)
                        if check_shooting_or_inverse is False:
                            print("...Inverse Hammer...")
                        else:
                            print("...Hammer...")

                    desired_loss = mt5.account_info()[10] * 0.01
                    reward: float = abs(tp - price) * 100
                    risk: float = abs(price - sl) * 100

                    lot = float(f'{desired_loss / risk:.2f}')
                    print(f"risk={risk:.2f}\treward={reward:.2f}\n"
                          f"desired_loss/risk\t{desired_loss:.2f}/{risk:.2f}={lot}")

                    request = {
                        'action': mt5.TRADE_ACTION_DEAL,
                        'symbol': symbol,
                        'volume': lot,
                        'type': type_of_order,
                        'price': price,
                        "sl": sl, 'tp': tp, 'type_time': mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_FOK
                    }
                    result = mt5.order_send(request)

                    if result.retcode == mt5.TRADE_RETCODE_DONE: counter += 1
                    print(
                        f'Third Candle: body->{candle3.body():.5f}\t'
                        f'upper shadow->{candle3.upper_shadow():.5f}\t'
                        f'lower shadow->{candle3.lower_shadow():.5f}\t'
                        f"close-> {third_candle['close']}"
                    )
                    # Second Candle
                    print(
                        f'Second Candle: body->{candle2.body():.5f}\t'
                        f'upper shadow->{candle2.upper_shadow():.5f}\t'
                        f'lower shadow->{candle2.lower_shadow():.5f}\t'
                        f"close-> {second_candle['close']}"
                    )
                    print("Number of order that has been sent: %d" % counter)
                    print(result)
                    print("=  =  =  =  =  =  =  =  =  =")
                else:
                    # Details of two candles
                    # Third Candle
                    print(
                        f'Third Candle: body->{candle3.body_of_candle():.5f}\t'
                        f'upper shadow->{candle3.upper_shadow():.5f}\t'
                        f'lower shadow->{candle3.lower_shadow():.5f}\t'
                        f"close-> {third_candle['close']}"
                    )
                    # Second Candle
                    print(
                        f'Second Candle: body->{candle2.body_of_candle():.5f}\t'
                        f'upper shadow->{candle2.upper_shadow():.5f}\t'
                        f'lower shadow->{candle2.lower_shadow():.5f}\t'
                        f"close-> {second_candle['close']}"
                    )
                    print("-  -  -  -  -  -  -  -  -  -")
                time.sleep(5)
        except KeyboardInterrupt:
            mt5.shutdown()
            sys.exit()
