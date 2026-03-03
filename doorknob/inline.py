import os
from rjsmin import jsmin
from rcssmin import cssmin
import logging

logger = logging.getLogger(__name__)

css: dict[str, str] = {}
js: dict[str, str] = {}

def load_css(path: str):
    logger.info(f"loading css from {path}")
    for style in os.listdir(path):
        if not style.endswith(".css"):
            continue

        with open(os.path.join(path, style), "r") as file:
            contents = file.read()
        name = style.removesuffix(".css")

        css[name] = str(cssmin(contents))
        logger.info(f"* {name}")

def load_js(path: str):
    logger.info(f"loading js from {path}")
    for script in os.listdir("./js"):
        if not script.endswith(".js"):
            continue

        with open(os.path.join("./js/", script), "r") as file:
            contents = file.read()
        name = script.removesuffix(".js")

        js[name] = str(jsmin(contents))
        logger.info(f"* {name}")

# TODO separate modules from scripts.

INLINE_PREFIX = "<!--inline start"
INLINE_SUFFIX = "inline end-->"

INJECT_PREFIX = "<!--inline inject start-->"
INJECT_SUFFIX = "<!--inline inject end-->"


def process_inline_block(inline_block: str) -> tuple[list[str], list[str]]:
    lines = inline_block.split("\n")
    scripts: list[str] = []
    stylesheets: list[str] = []

    for line in lines:
        if not line.strip():
            continue
        line = line.strip().split(":")
        inline_type = line[0].strip()
        required = line[1].strip()

        if inline_type == "js":
            if required not in js:
                logger.warning(f"! couldn't find script {required} - skipping!")
            scripts.append(required)
        elif inline_type == "css":
            if required not in css:
                logger.warning(f"! couldn't find stylesheet {required} - skipping!")
            stylesheets.append(required)

    return stylesheets, scripts


def autogen_block(stylesheets: list[str], scripts: list[str]):
    ret = ""

    for stylesheet in stylesheets:
        if stylesheet not in css:
            logger.warning(f"! could not find stylesheet {stylesheet} - skipping")
            continue
        ret += f"""
        <style>
{css[stylesheet]}
        </style>
"""

    for script in scripts:
        if script not in js:
            logger.warning(f"! could not find script {script} - skipping")
            continue
        ret += f"""
        <script>
{js[script]}
        </script>
"""

    return ret


def process_file(path: str):
    with open(path, "r") as file:
        contents = file.read()

    try:
        inline_block = contents.split(INLINE_PREFIX)[1]
        inline_block = inline_block.split(INLINE_SUFFIX)[0]
    except IndexError:
        logger.info(f"! {path} skipped!")
        return

    stylesheets, scripts = process_inline_block(inline_block)
    autogen = autogen_block(stylesheets, scripts)

    before = contents.split(INJECT_PREFIX)[0]
    after = contents.split(INJECT_SUFFIX)[1]

    new_file = f"""{before}{INJECT_PREFIX}
{autogen.strip("\n")}
        {INJECT_SUFFIX}{after}"""

    with open(path, "w") as file:
        _ = file.write(new_file)


    logger.info(f"* {path}")

def inline():
    logger.info("processing inline blocks")
    for root, _, files in os.walk(".", topdown=True):
        for file in files:
            if not file.endswith(".html"):
                continue
            process_file(os.path.join(root, file))
