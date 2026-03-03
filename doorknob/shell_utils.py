import os
import logging

logger = logging.getLogger(__name__)

class chdir:
    pwd: str
    dir: str

    def __init__(self, dir: str) -> None:
        self.pwd = os.getcwd()
        self.dir = dir

    def __enter__(self) -> None:
        logger.info(f"$ cd {self.dir}")
        self.pwd = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, *_) -> None:
        logger.info(f"$ cd {self.pwd}")
        os.chdir(self.pwd)
