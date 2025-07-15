"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from blacksheep.server.diagnostics import get_diagnostic_app
from blacksheep.server.redirects import get_trailing_slash_middleware
from rodi import Container

from app.auth import configure_authentication
from app.docs import configure_docs
from app.errors import configure_error_handlers
from app.logs import configure_logging
from app.services import configure_services
from app.settings import Settings
from app.templating import configure_templating
from blacksheepsqlalchemy import use_sqlalchemy


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(services=services)

    app.middlewares.append(get_trailing_slash_middleware())

    use_sqlalchemy(app, connection_string=settings.db_connection_string)

    app.serve_files("app/static")
    configure_logging()
    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_docs(app, settings)
    configure_templating(app, settings)
    return app


def get_app():
    try:
        return configure_application(*configure_services())
    except Exception as exc:
        return get_diagnostic_app(exc)


app = get_app()
