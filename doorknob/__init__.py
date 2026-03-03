from .dev import dev_remove
from .inline import inline, load_css, load_js
from .metadata import process_metadata
from .minify import minifier
from .feeds import build_feeds

__all__ = [
    "dev_remove",
    "inline",
    "load_css",
    "load_js",
    "process_metadata",
    "minifier",
    "build_feeds"
]

