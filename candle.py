class Candle:
    def __init__(self, high, low, c_open, c_close):
        self.high = high
        self.low = low
        self.c_open = c_open
        self.c_close = c_close

    def body(self) -> int:
        body = self.c_close - self.c_open
        return abs(body)

    def is_green_or_red(self) -> bool:
        if self.c_close > self.c_open:
            return True
        elif self.c_close < self.c_open:
            return False

    def upper_shadow(self) -> int:
        if self.is_green_or_red():
            return self.high - self.c_close
        else:
            return self.high - self.c_open

    def lower_shadow(self) -> int:
        if self.is_green_or_red():
            return self.c_open - self.low
        else:
            return self.c_close - self.low

    def length(self) -> int:
        return self.body() + self.upper_shadow() + self.lower_shadow()
