import time

from fastapi import FastAPI, Request


def add_response_time(app: FastAPI):
    use = app.middleware("http")
    use(process_time_middleware)


async def process_time_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(int(process_time * 1000)) + "ms"
    return response
