import os
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

import logging

logger = logging.getLogger(__name__)

IMAGE_EXTS = ["jpg", "jpeg", "png"]

MAX_WIDTH = 800
QUALITY = 84


def is_image(path: str) -> bool:
    ext = Path(path).suffix.lower().replace(".", "")
    return ext in IMAGE_EXTS


def optimize_image(image_path: str) -> str:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    new_path = path.with_suffix(".webp")

    if new_path.exists():
        return new_path.name

    with Image.open(path) as img:
        # resize
        if img.width > MAX_WIDTH:
            new_height = int(img.height * (MAX_WIDTH / img.width))
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # mode fix
        if img.mode in ("RGBA", "LA"):
            img = img.convert("RGBA")
        elif img.mode == "P":
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        img = ImageOps.exif_transpose(img)

        img.save(new_path, "WEBP", quality=QUALITY, method=6)

    return new_path.name


def process_file(path: str) -> None:
    logger.info(f"* {path}")
    html_path = Path(path)

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    imgs = soup.find_all("img")

    for img in imgs:
        src = img.get("src")

        if not src:
            continue
        if not is_image(src):
            continue

        image_path = html_path.parent / src

        if not image_path.exists():
            continue

        try:
            new_name = optimize_image(str(image_path))
            img["src"] = new_name
            logger.info(f"  {image_path} -> {new_name}")
        except Exception as e:
            logger.error(f"Failed optimizing {src}: {e}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


def image_optimizer():
    logger.info("optimizing images")
    for root, _, files in os.walk(".", topdown=True):
        for file in files:
            if not file.endswith(".html"):
                continue

            process_file(os.path.join(root, file))
