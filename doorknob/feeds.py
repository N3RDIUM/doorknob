from datetime import date, datetime, time, timezone
import json
from feedgen.feed import FeedGenerator
import logging

logger = logging.getLogger(__name__)

# TODO readtime with <!--content--> delimiters
# "readtime" in json feed and no support for rss/atom planned as of now.

def datetime_json_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def json_feed(filename, config, posts):
    feed = config
    feed["posts"] = posts

    with open(filename, "w") as f:
        _ = f.write(json.dumps(feed, default=datetime_json_serial))

# Very crude implementation, will fix when I'm not in a curry- i mean hurry.
def feedgen_feed(filename, config, posts):
    feed = FeedGenerator()
    feed.id(config.get("id", ""))
    feed.title(config.get("title", "Lorem Ipsum"))
    authors = config.get("authors", [])
    for author in authors:
        feed.author(author)
    feed.logo(config.get("logo", ""))
    feed.subtitle(config.get("subtitle", ""))
    links = config.get("links", [])
    for link in links:
        feed.link(**link)
    feed.language(config.get("language", "en"))

    for post in posts:
        fe = feed.add_entry()
        fe.id(post["url"])
        fe.title(post["title"])
        fe.description(post["description"])
        dt = datetime.combine(
            post["lastmod"], 
            time(),
            tzinfo=timezone.utc  # TODO configurable timezone
        )
        fe.updated(dt)
        # in case it was modified after publishing
        dt = datetime.combine(
            post.get("published", post["lastmod"]),
            time(),
            tzinfo=timezone.utc  # TODO configurable timezone
        )
        fe.published(dt)
        fe.link(href=post["url"])

    feed_type = config.get("type")
    if feed_type == "rss":
        feed.rss_file(filename)
    elif feed_type == "atom":
        feed.atom_file(filename)

feed_builders = {
    "json": json_feed,
    "rss": feedgen_feed,
    "atom": feedgen_feed
}

def build_feeds(pages, config) -> None:
    logger.info("feeds config found, processing feed posts from metadata")
    registered_feeds = config.keys()
    feed_entries = {}

    for page, metadata in pages.items():
        if not metadata:
            continue
        if "feeds" not in metadata:
            continue
        logger.info(f"* {page}")

        feeds = metadata["feeds"]
        for feed in feeds:
            if feed not in registered_feeds:
                logger.warning(f"! {page} references unknown feed {feed}, skip")
                continue
            if feed not in feed_entries:
                feed_entries[feed] = []
            feed_entries[feed].append(metadata)

    logger.info("building feed files")
    for feed, posts in feed_entries.items():
        feed_type = config[feed]["type"]
        if feed_type not in feed_builders:
            logger.error(f"! unknown feed type {feed_type}, skipping")
            continue

        feed_builders[feed_type](feed, config[feed], posts)
        logger.info(f"* {feed}")

