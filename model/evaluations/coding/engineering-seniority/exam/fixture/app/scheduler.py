from __future__ import annotations

from collections.abc import Callable


class Scheduler:
    def __init__(self) -> None:
        self._handlers: dict[str, Callable[[], None]] = {}

    def register(self, name: str, handler: Callable[[], None]) -> None:
        self._handlers[name] = handler

    def run(self, name: str) -> None:
        try:
            handler = self._handlers[name]
        except KeyError as error:
            raise ValueError(f"unknown scheduled task: {name}") from error
        handler()
