import os
import logging

logger = logging.getLogger(__name__)

def _find_replace(find: str, replace: str) -> None:
    try:
        _ = os.system(f"find -type f -exec sed -i 's/{find}/{replace}/g' {{}} +  ")
        logger.info(f"* {find} -> {replace}")
    except Exception as e:
        logger.info(f"! {find} -> {replace} error: {e}")

def find_replace(pairs) -> None:
    logger.info(f"processing find-replace entries")
    for find, replace in pairs.items():
        _find_replace(find, replace)

