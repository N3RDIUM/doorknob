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
    minifier
)

WELCOME = "doorknob, site builder and optimizer tailored for n3rdium.dev"
root_logger.info(WELCOME)

# load config
target = "./"
if os.path.exists("doorknob.json"):
    with open("doorknob.json", "r") as f:
        config = json.load(f)
    target = config["target"]
root_logger.info(f"target dir: {target}")

with chdir(target):
    load_css("css")
    load_js("js")

    process_metadata()
    dev_remove()
    inline()
    minifier()

