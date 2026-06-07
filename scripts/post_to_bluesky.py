# /// script
# requires-python = ">=3.14"
# dependencies = ["atproto==0.0.67"]
# ///
"""Post a blog entry to Bluesky and write the thread URI into frontmatter.

Usage:
    op run --env-file="./scripts/op.env" -- uv run scripts/post_to_bluesky.py content/blog/my-post/index.md

Environment:
    BSKY_HANDLE         Bluesky handle
    BSKY_APP_PASSWORD   Bluesky app password (from Settings > App Passwords)
"""

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import tomllib
from atproto import Client, exceptions, models


@dataclass
class BSkyConfig:
    bsky_handle: str
    bky_password: str


@dataclass
class Config:
    bsky: BSkyConfig
    markdown_path: Path
    config_path: Path
    base_url: str


@dataclass
class PostContent:
    frontmatter: list[str]
    body: list[str]


@dataclass
class Post:
    content: PostContent
    post_url: str


def parse_env() -> BSkyConfig:
    handle = os.environ.get("BSKY_HANDLE")
    password = os.environ.get("BSKY_APP_PASSWORD")

    if not handle:
        print("Error: Bluesky handle required. Set BSKY_HANDLE.", file=sys.stderr)
        sys.exit(1)
    if not password:
        print("Error: Bluesky app password required. Set BSKY_APP_PASSWORD.", file=sys.stderr)
        sys.exit(1)

    return BSkyConfig(bsky_handle=handle, bky_password=password)


def parse_arg_markdown_path(markdown_path: str) -> Path:
    if markdown_path is not None and not os.path.isfile(markdown_path):
        print(f"Error: File not found: {markdown_path}", file=sys.stderr)
        sys.exit(1)

    return Path(markdown_path)


def build_config() -> Config:
    bsky = parse_env()

    parser = argparse.ArgumentParser(description="Post to Bluesky and add thread URI to frontmatter")
    parser.add_argument("markdown_path", help="Path to the blog post markdown file")
    args = parser.parse_args()
    markdown_path = parse_arg_markdown_path(args.markdown_path)

    config_path = find_hugo_config()
    if not config_path:
        print("Error: Could not find hugo.toml", file=sys.stderr)
        sys.exit(1)

    base_url = read_baseurl(config_path)
    if not base_url:
        print(f"Error: Could not read baseURL from {config_path}", file=sys.stderr)
        sys.exit(1)

    return Config(bsky=bsky, markdown_path=markdown_path, config_path=config_path, base_url=base_url)


def find_hugo_config() -> Path | None:
    """Find hugo.toml starting from the script's location climbing up."""
    start = os.path.dirname(os.path.abspath(__file__))
    for parent in [start, *_parents(start)]:
        candidate = os.path.join(parent, "hugo.toml")
        if os.path.isfile(candidate):
            return Path(candidate)
    return None


def _parents(path):
    while True:
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
        yield parent


def read_baseurl(config_path: Path) -> str | None:
    """Extract baseURL from hugo.toml."""
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    return (data.get("baseURL") or "").rstrip("/") or None


def parse_content(raw: str) -> PostContent:
    lines = raw.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return PostContent(frontmatter=[], body=lines)
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return PostContent(frontmatter=[], body=lines)
    return PostContent(frontmatter=lines[1:end], body=lines[end + 1 :])


def get_title(header_lines):
    """Extract the title value from frontmatter header lines."""
    for line in header_lines:
        m = re.match(r'^title:\s*"(.+)"', line)
        if m:
            return m.group(1)
        m = re.match(r"^title:\s*'(.+)'", line)
        if m:
            return m.group(1)
        m = re.match(r"^title:\s*(.+)", line)
        if m:
            return m.group(1).strip()
    return None


def has_bluesky_uri(header_lines):
    return any(line.strip().startswith("bluesky_thread_uri:") for line in header_lines)


def add_or_update_bluesky_uri(header_lines, uri):
    new_uri_line = f'bluesky_thread_uri: "{uri}"\n'
    result = []
    replaced = False
    for line in header_lines:
        if line.strip().startswith("bluesky_thread_uri:"):
            result.append(new_uri_line)
            replaced = True
        else:
            result.append(line)
    if not replaced:
        result.append(new_uri_line)
    return result


def markdown_path_to_url(filepath, base_url, content_dir="content"):
    abs_file = os.path.abspath(filepath)
    abs_content = os.path.abspath(content_dir)
    rel = os.path.relpath(abs_file, abs_content)
    if rel.endswith("/index.md"):
        url_path = "/" + rel[:-9]
    elif rel.endswith(".md"):
        url_path = "/" + rel[:-3]
    else:
        url_path = "/" + rel
    return base_url + url_path


def at_uri_to_web_url(at_uri):
    m = re.match(r"at://(.+)/app\.bsky\.feed\.post/(.+)", at_uri)
    if not m:
        return at_uri
    return f"https://bsky.app/profile/{m.group(1)}/post/{m.group(2)}"


def parse_post_content(config: Config) -> Post:
    with open(config.markdown_path) as f:
        raw = f.read()

    content = parse_content(raw)
    title = get_title(content.frontmatter)
    if not title:
        print("Error: Could not find title in frontmatter", file=sys.stderr)
        sys.exit(1)

    post_url = markdown_path_to_url(
        config.markdown_path,
        config.base_url,
        content_dir=os.path.join(os.path.dirname(config.config_path), "content"),
    )
    post = Post(content=content, post_url=post_url)

    return post


def post_to_blue_sky(config: Config, post: Post, title: str) -> models.AppBskyFeedPost.CreateRecordResponse:
    text = f"New post: {title}\n\n{post.post_url}"

    url_start = text.index(post.post_url)
    url_bytes = post.post_url.encode("utf-8")
    byte_start = len(text[:url_start].encode("utf-8"))
    byte_end = byte_start + len(url_bytes)

    facets = [
        models.AppBskyRichtextFacet.Main(
            features=[models.AppBskyRichtextFacet.Link(uri=post.post_url)],
            index=models.AppBskyRichtextFacet.ByteSlice(
                byte_start=byte_start,
                byte_end=byte_end,
            ),
        )
    ]

    print("Posting to Bluesky")

    try:
        client = Client()
        client.login(config.bsky.bsky_handle, config.bsky.bky_password)
        post_ref = client.send_post(text, facets=facets)
    except (exceptions.AtProtocolError, ConnectionError, TimeoutError) as e:
        print(f"Error posting to Bluesky: {e}", file=sys.stderr)
        sys.exit(1)

    return post_ref


def update_post_after_bluesky_post(post_ref: models.AppBskyFeedPost.CreateRecordResponse, post: Post, config: Config):
    web_url = at_uri_to_web_url(post_ref.uri)
    print(f"Posted! {web_url}", file=sys.stderr)

    new_headers = add_or_update_bluesky_uri(post.content.frontmatter, web_url)

    with tempfile.NamedTemporaryFile(mode="w", dir=config.markdown_path.parent, delete=False) as f:
        tmp = f.name
        f.write("---\n")
        f.writelines(new_headers)
        f.write("---\n")
        f.writelines(post.content.body)

    os.replace(tmp, config.markdown_path)

    print(f"Updated {config.markdown_path} with bluesky_thread_uri", file=sys.stderr)
    print(web_url)


def main():
    config = build_config()
    post = parse_post_content(config)
    title = get_title(post.content.frontmatter)
    post_ref = post_to_blue_sky(config, post, title)
    update_post_after_bluesky_post(post_ref, post, config)


if __name__ == "__main__":
    main()
