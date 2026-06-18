#!/usr/bin/env python3
import json
import os
from html.parser import HTMLParser


class MetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.date = ""
        self._in_title = False
        self._head_done = False

    def handle_starttag(self, tag, attrs):
        if self._head_done:
            return
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs.get("name", "")
            prop = attrs.get("property", "")
            content = attrs.get("content", "")
            if name == "date":
                self.date = content
            elif name == "description" and not self.description:
                self.description = content
            elif prop == "og:description" and not self.description:
                self.description = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "head":
            self._head_done = True

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def extract_metadata(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    parser = MetaExtractor()
    parser.feed(content)

    return {
        "title": parser.title.strip() or os.path.basename(filepath),
        "description": parser.description.strip(),
        "date": parser.date.strip() or "1970-01-01",
        "path": f"src/{os.path.basename(filepath)}",
    }


def main():
    src_dir = "src"
    articles = []

    if os.path.isdir(src_dir):
        for filename in sorted(os.listdir(src_dir)):
            if filename.endswith(".html"):
                meta = extract_metadata(os.path.join(src_dir, filename))
                articles.append(meta)

    articles.sort(key=lambda x: x["date"], reverse=True)

    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Generated articles.json with {len(articles)} article(s)")


if __name__ == "__main__":
    main()
