"""
Example API implemented using a controller.
"""

from typing import Optional

from blacksheep.server.controllers import Controller, get

from domain.cookies import Cookie, CookiesManager


class FortuneCookies(Controller):
    manager: CookiesManager

    @classmethod
    def route(cls) -> Optional[str]:
        return "/api/cookies"

    @classmethod
    def class_name(cls) -> str:
        return "Fortune Cookies"

    @get("/pick")
    async def get_fortune_cookie(self) -> Cookie:
        """Returns a random fortune cookie."""
        return await self.manager.pick_random_cookie()
