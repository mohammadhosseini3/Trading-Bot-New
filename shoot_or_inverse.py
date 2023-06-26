from ConfirmationCandle import check_confirmation_candle


def shoot_or_inverse(body,
                     upper_shadow,
                     lower_shadow,
                     second_candle_trend) -> bool:
    """
    return True -> when Third candle is shooting and Second Candle is decreasing
    return False -> when Third Candle is inverse and Second Candle is Increasing
    return None -> When it is not shooting star or inverse hammer
    """

    flag = None
    if ((upper_shadow >= lower_shadow * 3) and
            (upper_shadow >= body * 2)):

        # Second Candle is decreasing
        if second_candle_trend is False:
            flag = True

        elif second_candle_trend is True:
            flag = False

    return flag


def is_shooting_or_inverse(third_candle_body,
                           upper_shadow,
                           lower_shadow,
                           second_candle_trend,
                           second_candle_close,
                           third_candle_close
                           ) -> bool:
    """
    shooting star -> return True
    inverse hammer -> return False
    none of them -> return none
    """

    # Determine if it is shooting or inverse before checking confirmation Candle
    result = shoot_or_inverse(third_candle_body,
                              upper_shadow,
                              lower_shadow,
                              second_candle_trend)

    is_confirmed = check_confirmation_candle(second_candle_close,
                                             second_candle_trend,
                                             third_candle_close)

    flag = None
    # When it is shooting star or inverse hammer and second candle is confirmed
    if result is not None and is_confirmed:

        # if result is true -> shooting star
        if result is True:
            flag = True

        # else -> inverse hammer
        else:
            flag = False

    return flag
