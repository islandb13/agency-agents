import os
from datetime import datetime, timedelta, timezone

import requests

USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "vanguard-1/0.1")
TIMEOUT = 20


class ImpedimentNeeded(RuntimeError):
    """Raised when a research call cannot proceed without an API key.
    The main loop catches this and routes it through memory.log_impediment()."""

    def __init__(self, resource: str, roi_impact: str):
        super().__init__(f"missing resource: {resource}")
        self.resource = resource
        self.roi_impact = roi_impact


def research_reddit(subreddit: str, query: str | None = None, limit: int = 25) -> dict:
    """Pull recent posts from a subreddit and surface likely pain points.

    Strategy:
      - If PRAW credentials are present, use them (stable, gated-sub access).
      - Otherwise hit the public .json endpoint (works but rate-limited to ~60 rpm).

    Heuristic pain-point filter: titles that start with 'how do', 'is there',
    'why does', 'anyone know', or contain 'frustrat', 'hate', 'broken',
    'wish there was', 'struggle'.
    """
    sub = subreddit.strip().lstrip("r/").strip("/")
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")

    posts: list[dict] = []
    source: str

    if client_id and client_secret:
        try:
            import praw  # local import: optional dep
        except ImportError as e:
            raise ImpedimentNeeded(
                resource="praw (pip install praw)",
                roi_impact="With PRAW we can scan gated/private subs and avoid public-JSON "
                           "rate limits, expanding the pain-point corpus ~5x.",
            ) from e
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=USER_AGENT,
        )
        source = "praw"
        listing = (
            reddit.subreddit(sub).search(query, limit=limit, time_filter="month")
            if query else reddit.subreddit(sub).hot(limit=limit)
        )
        for p in listing:
            posts.append({
                "title": p.title,
                "url": f"https://reddit.com{p.permalink}",
                "score": p.score,
                "num_comments": p.num_comments,
                "selftext": (p.selftext or "")[:500],
                "created_utc": p.created_utc,
            })
    else:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
        if query:
            url = (
                f"https://www.reddit.com/r/{sub}/search.json"
                f"?q={requests.utils.quote(query)}&restrict_sr=1&sort=new&limit={limit}"
            )
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        if r.status_code == 429:
            raise ImpedimentNeeded(
                resource="REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET",
                roi_impact="Hit public Reddit rate limit. Authed access removes the throttle "
                           "and ~5x scan throughput -> faster gap-finding cadence.",
            )
        r.raise_for_status()
        source = "public-json"
        for child in r.json().get("data", {}).get("children", []):
            d = child.get("data", {})
            posts.append({
                "title": d.get("title", ""),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "score": d.get("score", 0),
                "num_comments": d.get("num_comments", 0),
                "selftext": (d.get("selftext") or "")[:500],
                "created_utc": d.get("created_utc", 0),
            })

    markers = ("how do ", "is there ", "why does ", "anyone know",
               "frustrat", "hate ", "broken", "wish there was", "struggle")
    pain_points = [
        p for p in posts
        if any(m in (p["title"] + " " + p["selftext"]).lower() for m in markers)
    ]

    return {
        "subreddit": sub,
        "source": source,
        "query": query,
        "post_count": len(posts),
        "pain_point_count": len(pain_points),
        "pain_points": pain_points[:10],
    }


def research_github(query: str = "stars:>50", limit: int = 15, days: int = 14) -> dict:
    """Surface fast-rising repos via the GitHub search API.

    Builds a query of `{query} created:>{today-days}` sorted by stars, which is the
    standard proxy for 'trending'.  Works unauthenticated (60 req/hr) - Impediment
    Report raised if rate-limited.
    """
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"{query} created:>{since}"
    r = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": q, "sort": "stars", "order": "desc", "per_page": limit},
        headers=headers,
        timeout=TIMEOUT,
    )
    if r.status_code == 403 and "rate limit" in r.text.lower():
        raise ImpedimentNeeded(
            resource="GITHUB_TOKEN",
            roi_impact="Unauthed GitHub search is capped at 60 req/hr. A PAT lifts "
                       "this to 5,000 req/hr -> continuous trend scanning.",
        )
    r.raise_for_status()
    items = r.json().get("items", [])

    repos = [{
        "full_name": it["full_name"],
        "description": it.get("description") or "",
        "stars": it.get("stargazers_count", 0),
        "language": it.get("language"),
        "url": it.get("html_url"),
        "created_at": it.get("created_at"),
        "pushed_at": it.get("pushed_at"),
    } for it in items]

    return {
        "query": q,
        "authenticated": bool(token),
        "count": len(repos),
        "repos": repos,
    }
