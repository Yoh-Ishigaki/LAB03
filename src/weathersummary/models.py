class WeatherRecord:
    """Represent one validated hourly weather observation."""

    def __init__(self, time, temperature, precipitation):
        if not isinstance(time, str):
            raise ValueError("time must be a string")

        if (
            not isinstance(temperature, (int, float))
            or isinstance(temperature, bool)
        ):
            raise ValueError("temperature must be numeric")

        if (
            not isinstance(precipitation, (int, float))
            or isinstance(precipitation, bool)
        ):
            raise ValueError("precipitation must be numeric")

        self.time = time
        self.temperature = float(temperature)
        self.precipitation = float(precipitation)

    def __str__(self):
        return (
            f"WeatherRecord(time={self.time}, "
            f"temperature={self.temperature}, "
            f"precipitation={self.precipitation})"
        )
