from blacksheep.server.controllers import Controller, get

from domain.cookies import CookiesManager


class Home(Controller):
    manager: CookiesManager

    @get()
    async def index(self):
        return self.view(model={"cookie": await self.manager.pick_random_cookie()})
