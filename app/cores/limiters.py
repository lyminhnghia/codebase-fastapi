from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_ipaddr


def add_limiters(app: FastAPI):
    app.add_middleware(SlowAPIMiddleware)
    limiter = Limiter(key_func=get_ipaddr, default_limits=["50/second"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
