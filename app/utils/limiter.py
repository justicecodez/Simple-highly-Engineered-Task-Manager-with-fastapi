from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Limiter, Rate, Duration
from functools import lru_cache


@lru_cache()

def create_rate_limiter(
    requests: int,
    seconds: int
):
    limiter = Limiter(
        Rate(
            requests,
            Duration.SECOND * seconds
        )
    )

    return RateLimiter(
        limiter=limiter
    )