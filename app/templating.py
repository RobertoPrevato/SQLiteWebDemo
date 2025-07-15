import os

from blacksheep.server import Application
from blacksheep.server.rendering.jinja2 import JinjaRenderer
from blacksheep.settings.html import html_settings
from blacksheep.utils import join_fragments

from app.settings import Settings


def configure_templating(app: Application, settings: Settings) -> None:
    """
    Configures server side rendering for HTML views.
    """
    renderer = html_settings.renderer
    assert isinstance(renderer, JinjaRenderer)

    def get_bg_color():
        return os.environ.get("BG_COLOR", "#1abc9c")

    def abs_url(value: str = ""):
        prefix = app.router.prefix
        if not value and prefix and not prefix.endswith("/"):
            return prefix + "/"
        return join_fragments(prefix, value)

    renderer.env.globals.update({"bgcolor": get_bg_color, "absurl": abs_url})
