
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


TRACKING_PARAMS = {
    "fbclid",
    "gclid",
}


def normalize_url(url: str) -> str:
    """Normalize a URL to make duplicate detection more reliable."""

    if not url:
        return ""

    parsed = urlsplit(url.strip())

    # Remove common tracking parameters.
    query_params = [
        (key, value)
        for key, value in parse_qsl(parsed.query)
        if not key.lower().startswith("utm_")
        and key.lower() not in TRACKING_PARAMS
    ]

    normalized = urlunsplit((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        urlencode(query_params),
        "",  # Remove URL fragment.
    ))

    return normalized


def remove_duplicate_sources(sources: list[dict]) -> list[dict]:
    """Remove sources with duplicate normalized URLs."""

    unique_sources = []
    seen_urls = set()

    for source in sources:
        normalized = normalize_url(source.get("url", ""))

        # Keep sources without URLs rather than accidentally
        # treating every missing URL as the same source.
        if not normalized:
            unique_sources.append(source)
            continue

        if normalized in seen_urls:
            continue

        seen_urls.add(normalized)
        unique_sources.append(source)

    return unique_sources
