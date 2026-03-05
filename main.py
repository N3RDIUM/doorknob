import os
import json
from .doorknob.logger import root_logger
from .doorknob.shell_utils import chdir
from .doorknob import (
    load_js, 
    load_css,
    process_metadata,
    dev_remove,
    inline,
    minifier,
    build_feeds,
    find_replace
)

WELCOME = "doorknob, site builder and optimizer tailored for n3rdium.dev"
root_logger.info(WELCOME)

# load config
target = "./"
config = {}
if os.path.exists("doorknob.json"):
    with open("doorknob.json", "r") as f:
        config = json.load(f)
    target = config["target"]
root_logger.info(f"target dir: {target}")

with chdir(target):
    load_css("css")
    load_js("js")

    pages = process_metadata()
    dev_remove()
    inline()
    minifier()

    feeds_config = config.get("feeds")
    if feeds_config is not None:
        build_feeds(pages, feeds_config)

    find_replace_pairs = config.get("find_replace")
    if find_replace_pairs is not None:
        find_replace(find_replace_pairs)

