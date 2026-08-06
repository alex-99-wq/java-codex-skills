#!/usr/bin/env python3
"""Calculate the next spaced-review date for java-backend-vibe-upskill."""

from __future__ import annotations

import argparse
import json
import math
from datetime import date, datetime, timedelta


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD") from exc


def next_interval(score: int, current_interval_days: int) -> int:
    if current_interval_days < 1:
        raise ValueError("current interval must be at least 1 day")
    if score == 0:
        return 1
    if score == 1:
        return max(1, math.ceil(current_interval_days / 2))
    if score == 2:
        return min(120, current_interval_days * 2)
    raise ValueError("score must be 0, 1, or 2")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate next review date from mastery score and current interval."
    )
    parser.add_argument("--score", type=int, required=True, choices=[0, 1, 2])
    parser.add_argument("--current-interval-days", type=int, default=1)
    parser.add_argument("--date", type=parse_date, default=date.today())
    args = parser.parse_args()

    interval = next_interval(args.score, args.current_interval_days)
    next_date = args.date + timedelta(days=interval)

    print(
        json.dumps(
            {
                "score": args.score,
                "current_interval_days": args.current_interval_days,
                "next_interval_days": interval,
                "next_review_date": next_date.isoformat(),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
