import os
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
import logging

logger = logging.getLogger(__name__)

def _highlight(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for code in soup.select("pre > code"):
        code_text = code.get_text()

        lang = None
        for cls in code.get("class", []):
            if cls.startswith("language-"):
                lang = cls.replace("language-", "")
                break

        try:
            lexer = get_lexer_by_name(lang) if lang else guess_lexer(code_text)
        except Exception:
            lexer = guess_lexer(code_text)

        formatter = HtmlFormatter(nowrap=True, cssclass="syntax")

        highlighted = highlight(code_text, lexer, formatter)

        code.clear()
        code.append(BeautifulSoup(highlighted, "html.parser"))

    return str(soup)

def process_file(path: str) -> None:
    with open(path, "r") as f:
        contents = f.read()
    highlighted = _highlight(contents)
    with open(path, "w") as f:
        _ = f.write(highlighted)
    logger.info(f"* {path}")

def syntax_highlighter() -> None:
    logger.info("syntax highlighting")
    for root, _, files in os.walk(".", topdown=True):
        for file in files:
            if not file.endswith(".html"):
                continue
            process_file(os.path.join(root, file))
