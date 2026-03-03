import os
import minify_html
import logging

logger = logging.getLogger(__name__)

def minify(source: str) -> str:
    return minify_html.minify(
        source, 
        minify_js=True, 
        remove_processing_instructions=True
    )

def minify_file(path: str) -> None:
    with open(path, "r") as file:
        contents = file.read()
        minified = minify(contents)

    with open(path, "w") as file:
        _ = file.write(minified)
        logger.info(f"* {path}")

def minifier():
    logger.info("minifying html")
    for root, _, files in os.walk(".", topdown=True):
        for file in files:
            if not file.endswith(".html"):
                continue
            minify_file(os.path.join(root, file))

