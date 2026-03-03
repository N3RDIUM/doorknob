import os
import yaml
from datetime import date
import logging

logger = logging.getLogger(__name__)

type Metadata = dict[str, str | int | float | None]
type URL = str
pages: dict[URL, Metadata] = {}

META_PREFIX = "<!--meta start"
META_SUFFIX = "meta end-->"

def urlify(path: str) -> URL:
    # TODO make toplevel url configurable
    return "https://n3rdium.dev/" + path \
        .removeprefix(".") \
        .removeprefix("/") \
        .removesuffix("index.html")

def extract_metadata(file: str):
    with open(file, "r") as f:
        contents = f.read()

    try:
        raw_yaml = contents.split(META_PREFIX)[1].split(META_SUFFIX)[0]
        metadata: Metadata = yaml.safe_load(raw_yaml)
        url = urlify(file)
        metadata["url"] = url
        pages[url] = metadata
        logger.info(f"* {file}")
    except IndexError as e:
        logger.warning(f"! {file} IndexError: {e}")
        return
    except Exception as e:
        logger.warning(f"! {file} Exception: {e}")
        return

DEFAULT_LASTMOD = date.today().strftime("%Y-%m-%d")
DEFAULT_CHANGEFREQ = "never"
DEFAULT_PRIORITY = 0.5

def build_sitemap_entry(url: URL, metadata: Metadata) -> str:
    lastmod = metadata.get("lastmod", DEFAULT_LASTMOD)
    changefreq = metadata.get("changefreq", DEFAULT_CHANGEFREQ)
    priority = metadata.get("priority", DEFAULT_PRIORITY)

    return f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>{changefreq}</changefreq>
        <priority>{priority}</priority>
    </url>"""

def build_sitemap() -> str:
    entries: list[str] = []

    for url, metadata in pages.items():
        if metadata is None:
            logger.warning(f"! {url} [no metadata]")
            continue
        if metadata.get("sitemap_invisible"):
            logger.info(f"* {url} [invisible]")
            continue
        entries.append(build_sitemap_entry(url, metadata))
        logger.info(f"* {url}")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(entries)}
</urlset>
"""

def process_metadata():
    logger.info("processing metadata")
    for root, _, files in os.walk(".", topdown=True):
        for file in files:
            if not file.endswith(".html"):
                continue
            extract_metadata(os.path.join(root, file))
    
    sitemap_path = "sitemap.xml"
    logger.info(f"building main sitemap {sitemap_path}")
    sitemap = build_sitemap()
    with open(sitemap_path, "w") as f:
        _ = f.write(sitemap)

    return pages

