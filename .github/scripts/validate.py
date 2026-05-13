#!/usr/bin/env python3
"""Validate every entry under entries/ against the schema in products.yml.

Exits non-zero with a human-readable error list when any file fails.
"""
from __future__ import annotations

import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRIES_DIR = REPO_ROOT / "entries"
CONFIG_PATH = REPO_ROOT / "products.yml"

FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ALLOWED_TAGS = {"new", "improved", "beta"}
TITLE_MAX = 80
DESCRIPTION_MAX = 200
BODY_WORD_MAX = 400
EMOJI_MAX_LEN = 8  # accommodates ZWJ sequences like 👨‍👩‍👧
EARLIEST_DATE = date(2020, 1, 1)

FORBIDDEN_TAGS = ("script", "iframe", "style", "object", "embed", "link", "meta")
FORBIDDEN_TAG_RE = re.compile(
    r"<\s*(" + "|".join(FORBIDDEN_TAGS) + r")\b", re.IGNORECASE
)

# Internal jargon that should never appear in customer-facing copy.
JIRA_TICKET_RE = re.compile(r"\bAI-\d{2,6}\b")
SLACK_URL_RE = re.compile(r"https?://[a-z0-9-]+\.slack\.com/", re.IGNORECASE)
TODO_MARKER_RE = re.compile(r"\b(TODO|FIXME|XXX)\b")

LINK_RE = re.compile(r"!?\[[^\]]*\]\((\S+?)(?:\s+\"[^\"]*\")?\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((\S+?)(?:\s+\"[^\"]*\")?\)")
AUTOLINK_RE = re.compile(r"<((?:https?)://[^>\s]+)>")
# Bare URL excludes closing quotes/brackets so HTML-attribute residue
# (e.g. src="https://x.com") doesn't pollute the captured URL.
BARE_URL_RE = re.compile(r"(?<![(<\w])(https?://[^\s)<>\"']+)")

# Heading lines (#, ##, etc.) — bodies should never start with one because
# the rendered card already shows the title as the heading.
LEADING_HEADING_RE = re.compile(r"^\s*#{1,6}\s+\S", re.MULTILINE)

ALLOWED_FRONTMATTER_KEYS = {
    "title", "date", "products", "tag", "emoji", "hero", "draft", "description",
}


def load_config() -> dict:
    with CONFIG_PATH.open() as fh:
        config = yaml.safe_load(fh)
    return {
        "product_slugs": {p["slug"] for p in config.get("products", [])},
        "allowed_hosts": {h.lower() for h in config.get("allowed_hosts", [])},
    }


def host_allowed(url: str, allowed_hosts: set[str]) -> bool:
    try:
        host = urlparse(url).hostname or ""
    except ValueError:
        return False
    return host.lower() in allowed_hosts


def parse_iso_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def check_filename(rel: Path, name: str) -> tuple[list[str], str | None]:
    errors: list[str] = []
    match = FILENAME_RE.match(name)
    if not match:
        errors.append(
            f"{rel}: filename must match YYYY-MM-DD-kebab-slug.md (got {name})"
        )
        return errors, None
    return errors, f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


def check_frontmatter(
    rel: Path, front: dict, filename_date: str, config: dict
) -> list[str]:
    errors: list[str] = []

    # title
    title = front.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"{rel}: title is required and must be a non-empty string")
    elif len(title) > TITLE_MAX:
        errors.append(f"{rel}: title is {len(title)} chars (max {TITLE_MAX})")
    elif title != title.strip():
        errors.append(f"{rel}: title has leading/trailing whitespace")

    # date — must be present, ISO, match filename, not in the future, post-2020
    date_value = front.get("date")
    date_str = str(date_value) if date_value is not None else ""
    parsed_date: date | None = None
    if not ISO_DATE_RE.match(date_str):
        errors.append(f"{rel}: date is required and must be YYYY-MM-DD")
    else:
        parsed_date = parse_iso_date(date_str)
        if parsed_date is None:
            errors.append(f"{rel}: date {date_str} is not a real calendar date")
        else:
            if date_str != filename_date:
                errors.append(
                    f"{rel}: frontmatter date ({date_str}) must match "
                    f"filename date ({filename_date})"
                )
            today_utc = datetime.now(timezone.utc).date()
            if parsed_date > today_utc + timedelta(days=1):
                errors.append(
                    f"{rel}: date {date_str} is in the future. "
                    f"Use today's date or backdate to the actual ship date."
                )
            if parsed_date < EARLIEST_DATE:
                errors.append(
                    f"{rel}: date {date_str} is before {EARLIEST_DATE.isoformat()}. "
                    f"Looks like a typo."
                )

    # products — non-empty list of known slugs
    products = front.get("products")
    if not isinstance(products, list) or not products:
        errors.append(f"{rel}: products is required and must be a non-empty list")
    else:
        unknown = [p for p in products if p not in config["product_slugs"]]
        if unknown:
            valid = ", ".join(sorted(config["product_slugs"]))
            errors.append(
                f"{rel}: unknown product(s) {unknown}. Allowed: {valid}"
            )
        if len(products) != len(set(products)):
            errors.append(f"{rel}: products list has duplicates")

    # emoji
    emoji = front.get("emoji")
    if not isinstance(emoji, str) or not emoji:
        errors.append(f"{rel}: emoji is required")
    elif len(emoji) > EMOJI_MAX_LEN:
        errors.append(
            f"{rel}: emoji must be a single character/sequence "
            f"(got {len(emoji)} chars)"
        )

    # description (optional one-line preview)
    description = front.get("description")
    if description is not None:
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{rel}: description must be a non-empty string if present")
        elif len(description) > DESCRIPTION_MAX:
            errors.append(
                f"{rel}: description is {len(description)} chars (max {DESCRIPTION_MAX})"
            )

    # tag (optional)
    tag = front.get("tag")
    if tag is not None and tag not in ALLOWED_TAGS:
        errors.append(
            f"{rel}: tag must be one of {sorted(ALLOWED_TAGS)} (got {tag!r})"
        )

    # draft (optional)
    draft = front.get("draft")
    if draft is not None and not isinstance(draft, bool):
        errors.append(f"{rel}: draft must be a boolean if present")

    # hero (optional)
    hero = front.get("hero")
    if hero is not None:
        if not isinstance(hero, str):
            errors.append(f"{rel}: hero must be a URL string")
        elif not hero.startswith("https://"):
            errors.append(f"{rel}: hero URL must use https:// ({hero})")
        elif not host_allowed(hero, config["allowed_hosts"]):
            errors.append(f"{rel}: hero URL host not in allowed_hosts ({hero})")

    extra = set(front) - ALLOWED_FRONTMATTER_KEYS
    if extra:
        errors.append(
            f"{rel}: unknown frontmatter key(s) {sorted(extra)} — "
            f"allowed: {sorted(ALLOWED_FRONTMATTER_KEYS)}"
        )

    return errors


def check_body(rel: Path, body: str, config: dict) -> list[str]:
    errors: list[str] = []

    stripped = body.strip()
    if not stripped:
        errors.append(f"{rel}: body is empty — add at least one sentence")
        return errors

    # The card already renders the title — bodies should open with prose,
    # not another heading.
    if LEADING_HEADING_RE.match(stripped):
        errors.append(
            f"{rel}: body must not start with a Markdown heading "
            f"(the entry title is already the heading)"
        )

    word_count = len(body.split())
    if word_count > BODY_WORD_MAX:
        errors.append(
            f"{rel}: body is {word_count} words (max {BODY_WORD_MAX}). "
            f"Trim or split into multiple entries."
        )

    if FORBIDDEN_TAG_RE.search(body):
        errors.append(
            f"{rel}: raw HTML <script|iframe|style|object|embed|link|meta> "
            f"tags are not allowed in the body"
        )

    if JIRA_TICKET_RE.search(body):
        errors.append(
            f"{rel}: body contains a Jira ticket reference (AI-XXXX). "
            f"Translate to plain language before publishing."
        )
    if SLACK_URL_RE.search(body):
        errors.append(
            f"{rel}: body contains a Slack URL. "
            f"Internal links don't belong in customer-facing copy."
        )
    if TODO_MARKER_RE.search(body):
        errors.append(
            f"{rel}: body contains TODO/FIXME/XXX. "
            f"Finish the draft before merging."
        )

    # Images need alt text — accessibility + screenshot context.
    for alt, _url in IMAGE_RE.findall(body):
        if not alt.strip():
            errors.append(
                f"{rel}: image is missing alt text. Describe what's in the image."
            )

    # Trailing whitespace on any line.
    for line_no, line in enumerate(body.splitlines(), start=1):
        if line != line.rstrip():
            errors.append(f"{rel}: trailing whitespace on line {line_no}")
            break  # one report is enough — markdownlint will list all

    # Tabs.
    if "\t" in body:
        errors.append(f"{rel}: body contains tabs — use spaces only")

    # Link host allowlist + https-only.
    urls: set[str] = set()
    urls.update(LINK_RE.findall(body))
    urls.update(AUTOLINK_RE.findall(body))
    urls.update(BARE_URL_RE.findall(body))
    for url in urls:
        if url.startswith(("#", "mailto:", "/")):
            continue
        if not url.startswith(("http://", "https://")):
            continue
        if url.startswith("http://"):
            errors.append(f"{rel}: http:// links are not allowed ({url})")
            continue
        if not host_allowed(url, config["allowed_hosts"]):
            errors.append(f"{rel}: link host not in allowed_hosts ({url})")

    return errors


def validate_entry(path: Path, config: dict) -> list[str]:
    rel = path.relative_to(REPO_ROOT)
    errors, filename_date = check_filename(rel, path.name)
    if filename_date is None:
        return errors

    raw = path.read_text(encoding="utf-8")

    if "\r\n" in raw:
        errors.append(f"{rel}: file has CRLF line endings — use LF only")

    fm_match = FRONTMATTER_RE.match(raw)
    if not fm_match:
        errors.append(f"{rel}: missing YAML frontmatter delimited by ---")
        return errors

    try:
        front = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{rel}: frontmatter is not valid YAML — {e}")
        return errors

    if not isinstance(front, dict):
        errors.append(f"{rel}: frontmatter must be a YAML mapping")
        return errors

    errors.extend(check_frontmatter(rel, front, filename_date, config))
    errors.extend(check_body(rel, fm_match.group(2), config))

    return errors


def main() -> int:
    if not ENTRIES_DIR.exists():
        print("entries/ directory not found — nothing to validate", file=sys.stderr)
        return 0

    config = load_config()
    all_errors: list[str] = []
    files = sorted(ENTRIES_DIR.glob("*.md"))

    if not files:
        print("No entries found.")
        return 0

    for path in files:
        all_errors.extend(validate_entry(path, config))

    if all_errors:
        print(f"Found {len(all_errors)} validation error(s):\n", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} entries — all good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
