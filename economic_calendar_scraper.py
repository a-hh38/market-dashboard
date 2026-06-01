import re
import requests
import pandas as pd
from playwright.sync_api import sync_playwright

FOREX_FACTORY_URL = "https://www.forexfactory.com/calendar"

G10 = [
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "AUD",
    "CAD",
    "NZD",
    "CHF"
]


def discover_feed_url():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        )

        page.goto(
            FOREX_FACTORY_URL,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()

        browser.close()

    match = re.search(
        r'https://nfs\.faireconomy\.media/ff_calendar_thisweek\.json\?version=[a-zA-Z0-9]+',
        html
    )

    if not match:
        raise Exception(
            "Could not locate Forex Factory JSON feed."
        )

    return match.group(0)


def get_calendar():

    feed_url = discover_feed_url()

    print(f"Feed Found:\n{feed_url}\n")

    response = requests.get(
        feed_url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    for col in [
        "actual",
        "forecast",
        "previous",
        "impact",
        "country",
        "title"
    ]:
        if col not in df.columns:
            df[col] = ""

    return df


if __name__ == "__main__":

    df = get_calendar()

    df.to_csv(
        "economic_calendar_full.csv",
        index=False
    )

    dashboard_df = df[
        (df["country"].isin(G10))
        &
        (df["impact"].isin(["Medium", "High"]))
    ]

    dashboard_df.to_csv(
        "economic_calendar_dashboard.csv",
        index=False
    )

    print(f"Total Events: {len(df)}")
    print(f"Dashboard Events: {len(dashboard_df)}")

    print("\nUpcoming High Impact Events:\n")

    print(
        dashboard_df[
            [
                "date",
                "country",
                "impact",
                "title",
                "actual",
                "forecast",
                "previous"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )