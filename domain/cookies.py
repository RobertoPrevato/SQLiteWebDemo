import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from essentials.exceptions import ObjectNotFound


logger = logging.getLogger("app")


@dataclass
class Cookie:
    id: int
    text: str


class CookieRepository(ABC):
    """Abstract base class for cookie repository."""

    @abstractmethod
    async def pick_random(self) -> Cookie:
        """Pick a random cookie."""


class CookiesManager:
    """Manages cookies using a repository."""

    def __init__(self, repository: CookieRepository):
        self.repository = repository

    async def pick_random_cookie(self) -> Cookie:
        """Pick a random cookie from the repository."""
        cookie = await self.repository.pick_random()

        if cookie is None:
            # should never happen, but just in case...
            raise ObjectNotFound()

        logger.info("Picked cookie: %s", cookie.text)
        return cookie
