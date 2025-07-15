from rodi import Container
from domain.cookies import CookieRepository
from data.sql.cookies import SQLiteCookieRepository


def register_sql_services(container: Container) -> None:
    container.add_scoped(
        CookieRepository,
        SQLiteCookieRepository,
    )
