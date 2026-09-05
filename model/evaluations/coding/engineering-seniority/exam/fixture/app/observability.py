from __future__ import annotations

import json
import logging


class RequestLogger:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("fixture.api")

    def log_request(self, method: str, path: str, status: int, trace_id: str) -> None:
        self.logger.info(
            json.dumps(
                {
                    "method": method,
                    "path": path,
                    "status": status,
                    "trace_id": trace_id,
                },
                sort_keys=True,
            )
        )
