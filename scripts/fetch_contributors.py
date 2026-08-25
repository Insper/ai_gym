"""Fetch repository contributors for the MkDocs community page."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


OUTPUT = Path("docs/assets/data/contributors.json")


def fetch_contributors(repository: str, token: str) -> list[dict[str, object]]:
    contributors: list[dict[str, object]] = []
    page = 1

    while True:
        query = urlencode({"anon": "false", "per_page": 100, "page": page})
        url = f"https://api.github.com/repos/{repository}/contributors?{query}"
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "ai-gym-docs",
                "X-GitHub-Api-Version": "2022-11-28",
                **({"Authorization": f"Bearer {token}"} if token else {}),
            },
        )

        with urlopen(request, timeout=30) as response:  # noqa: S310
            batch = json.load(response)

        contributors.extend(
            {
                "login": item["login"],
                "avatar_url": item["avatar_url"],
                "html_url": item["html_url"],
                "contributions": item["contributions"],
            }
            for item in batch
            if item.get("type") == "User"
            and not item.get("login", "").endswith("[bot]")
        )

        if len(batch) < 100:
            break
        page += 1

    return contributors


def main() -> None:
    repository = os.environ.get("GITHUB_REPOSITORY", "Insper/ai_gym")
    token = os.environ.get("GITHUB_TOKEN", "")
    try:
        contributors = fetch_contributors(repository, token)
    except HTTPError as error:
        raise SystemExit(f"GitHub API request failed: {error.code} {error.reason}") from error

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(contributors, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(contributors)} contributors to {OUTPUT}")


if __name__ == "__main__":
    main()
