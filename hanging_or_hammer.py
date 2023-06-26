from ConfirmationCandle import check_confirmation_candle


def check_hanging_or_hammer(body, upper_shadow, lower_shadow, second_candle_trend) -> bool:
    """
       return True -> when Third candle is hanging man and Second Candle is decreasing
       return False -> when Third Candle is hammer and Second Candle is Increasing
       return None -> When it is not shooting star or inverse hammer
       """

    flag = None
    if ((upper_shadow * 3 <= lower_shadow) and
            (lower_shadow >= body * 2)):

        # Second Candle is decreasing
        if second_candle_trend is False:
            flag = True

        elif second_candle_trend is True:
            flag = False

    return flag


def is_hanging_or_hammer(third_candle_body,
                         upper_shadow,
                         lower_shadow,
                         second_candle_trend,
                         second_candle_close,
                         third_candle_close) -> bool:

    result = check_hanging_or_hammer(third_candle_body,
                                     upper_shadow,
                                     lower_shadow,
                                     second_candle_trend)

    is_confirmed = check_confirmation_candle(second_candle_close,
                                             second_candle_trend,
                                             third_candle_close)

    flag = None
    # When it is hanging man or hammer and second candle is confirmed
    if result is not None and is_confirmed:

        # if result is true -> hanging man
        if result is True:
            flag = True

        # else -> hammer
        else:
            flag = False

    return flag
