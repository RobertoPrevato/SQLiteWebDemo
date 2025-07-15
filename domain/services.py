from rodi import Container
from domain.cookies import CookiesManager


def register_handlers(container: Container) -> None:
    container.add_scoped(CookiesManager)
