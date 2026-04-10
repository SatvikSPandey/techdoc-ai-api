import time
from typing import Dict


class MetricsTracker:
    """
    Simple in-memory metrics tracker.

    Tracks request counts and response times while the container is running.
    Resets when the container restarts — that is fine for our use case.
    For persistent metrics in production you would use Prometheus or CloudWatch.
    """

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time_ms = 0.0
        self.start_time = time.time()

    def record_request(self, success: bool, response_time_ms: float):
        self.total_requests += 1
        self.total_response_time_ms += response_time_ms
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

    def get_metrics(self) -> Dict:
        avg_response_time = (
            round(self.total_response_time_ms / self.total_requests, 2)
            if self.total_requests > 0
            else 0.0
        )
        return {
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "average_response_time_ms": avg_response_time,
        }


# Singleton — import this in routes to record metrics
tracker = MetricsTracker()