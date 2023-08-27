def candlestick_type(body,
                     upper_shadow,
                     lower_shadow,
                     first_candle_color,
                     third_candle_color,
                     second_candle_close,
                     third_candle_close,
                     trend,
                     second_candle_color,
                     second_candle_open) -> str:

    # it can be shooting star or inverted hammer
    if (first_candle_color and second_candle_color and third_candle_color) is not None:
        if ((upper_shadow >= lower_shadow * 2) and
                (upper_shadow >= body * 2)):
            if first_candle_color and not third_candle_color and trend:
                if ((second_candle_color and third_candle_close < second_candle_open) or
                        (not second_candle_color and third_candle_close < second_candle_close)):
                    return "Shooting Star"

            elif (not first_candle_color and third_candle_color) and not trend:
                if ((second_candle_color and third_candle_close > second_candle_close) or
                        (not second_candle_color and third_candle_close > second_candle_open)):
                    return "Inverted Hammer"

        # it can be hanging man or hammer
        elif ((lower_shadow >= upper_shadow * 2) and
              (lower_shadow >= body * 2)):
            if first_candle_color and not third_candle_color and trend:
                if ((second_candle_color and third_candle_close < second_candle_open) or
                        (not second_candle_color and third_candle_close < second_candle_close)):
                    return "Hanging Man"
            elif not first_candle_color and third_candle_color and not trend:
                if ((second_candle_color and third_candle_close > second_candle_close) or
                        (not second_candle_color and third_candle_close > second_candle_open)):
                    return "Hammer"
