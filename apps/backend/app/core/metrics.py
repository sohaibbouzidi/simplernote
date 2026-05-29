import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.types import ASGIApp, Receive, Scope, Send

request_count = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
request_duration = Histogram("http_request_duration_seconds", "HTTP request duration", ["method", "path"])


class PrometheusMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "/")

        start = time.perf_counter()

        sent_status = [200]

        async def _send(message):
            if message["type"] == "http.response.start":
                sent_status[0] = message["status"]
            await send(message)

        await self.app(scope, receive, _send)

        duration = time.perf_counter() - start
        request_count.labels(method=method, path=path, status=sent_status[0]).inc()
        request_duration.labels(method=method, path=path).observe(duration)


def metrics_response():
    from starlette.responses import Response
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
