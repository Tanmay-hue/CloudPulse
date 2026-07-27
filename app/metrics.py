from prometheus_client import Counter, generate_latest
from fastapi import Response

REQUEST_COUNT = Counter(
    "cloudpulse_requests_total",
    "Total API Requests"
)


def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )