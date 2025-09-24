"""
APIs to test OTEL integration.
"""

import asyncio
import logging
import random
from typing import Optional

from blacksheep import Request, Response
from blacksheep.server.controllers import Controller, get
from blacksheep.server.otel import logcall
from opentelemetry import trace

logger = logging.getLogger(__name__)


@logcall("Example")
async def dependency_example():
    await asyncio.sleep(random.uniform(0.1, 1.5))


class OTELTests(Controller):
    @classmethod
    def route(cls) -> Optional[str]:
        return "/api/otel-tests"

    @classmethod
    def class_name(cls) -> str:
        return "OTEL Tests"

    @get("/test")
    async def test(self, request: Request) -> Response:
        """
        Logs a warning, a dependency call with random delay between 0.1 and 1.5s,
        and an extra trace for the request.
        """
        # logger.warning appear in the traces table
        logger.warning("Example warning")
        await dependency_example()

        # Add custom information to the current span
        span = trace.get_current_span()
        if span is not None:
            span.set_attribute("custom.info", "This is extra info for the request")
            span.add_event(
                "Custom event: home handler called",
                {"user_agent": request.headers.get(b"user-agent")[0].decode()},
            )

        return self.text("Hello, this is traced!")

    @get("/{name}")
    async def greetings(self, name: str) -> Response:
        """Returns an 'Hello, {name}' message."""
        logger.info("Saying Hi to %s", name)
        return self.text(f"Hello, {name}!")

    @get("/crash")
    async def crash_test(self):
        """Raises an exception to see how they get logged."""
        raise RuntimeError("Crash test!")
