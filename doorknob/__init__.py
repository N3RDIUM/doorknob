from .dev import dev_remove
from .inline import inline, load_css, load_js
from .metadata import process_metadata
from .minify import minifier

__all__ = [
    "dev_remove",
    "inline",
    "load_css",
    "load_js",
    "process_metadata",
    "minifier"
]

