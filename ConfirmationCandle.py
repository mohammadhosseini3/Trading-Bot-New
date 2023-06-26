def check_confirmation_candle(second_candle_close,
                              second_candle_trend,
                              third_candle_close) -> bool:
    """
    Determine if the second candle is suitable for
    confirmation or not.
    confirmation body > spread+commission and conf_close>shoot_or_inverse_close
    """

    confirmation = False
    # if second_candle_body >= broker:
    if (second_candle_trend is True and
        second_candle_close > third_candle_close) or \
            (second_candle_trend is False and
             second_candle_close < third_candle_close):
        confirmation = True

    return confirmation
