"""
Use this module to register required services.
Services registered inside a `rodi.Container` are automatically injected into request
handlers.

For more information and documentation, see `rodi` Wiki and examples:
    https://github.com/Neoteroi/rodi/wiki
    https://github.com/Neoteroi/rodi/tree/main/examples
"""

from typing import Tuple

from rodi import Container

from app.settings import Settings, load_settings
from data.sql.services import register_sql_services
from domain.services import register_handlers


def configure_services() -> Tuple[Container, Settings]:
    container = Container()
    settings = load_settings()

    container.add_instance(settings)

    register_sql_services(container)
    register_handlers(container)

    return container, settings
