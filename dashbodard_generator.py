from jinja2 import Environment, FileSystemLoader
import pandas as pd
from corporate_news_fetcher import fetch_corporate_news
from bulk_deals_fetcher import fetch_bulk_deals
from economic_snippets import generate_economic_snippets
from market_commentary import generate_commentary
from database import engine


def generate_dashboard():
    bulk_deals = fetch_bulk_deals()

    print("Loading dashboard datasets...")

    indian_markets = pd.read_sql(
        "SELECT * FROM indian_markets",
        engine
    )

    global_markets = pd.read_sql(
        "SELECT * FROM global_markets",
        engine
    )

    commodities = pd.read_sql(
        "SELECT * FROM commodities",
        engine
    )

    fxgsec = pd.read_sql(
        "SELECT * FROM fxgsec",
        engine
    )

    gainers = pd.read_sql(
        "SELECT * FROM top_gainers",
        engine
    )

    losers = pd.read_sql(
        "SELECT * FROM top_losers",
        engine
    )

    try:

        economic_calendar = pd.read_csv(
            "economic_calendar_dashboard.csv"
        )

    except Exception:

        economic_calendar = pd.DataFrame()

    try:

        economic_data = pd.read_csv(
            "economic_data.csv"
        )

    except Exception:

        economic_data = pd.DataFrame()

    try:

        participants = pd.read_csv(
            "participants_activity.csv"
        )

    except Exception:

        participants = pd.DataFrame()

    released_events = pd.DataFrame()
    upcoming_events = pd.DataFrame()

    if not economic_calendar.empty:

        # Released events

        released_events = economic_calendar.copy()

        economic_snippets = generate_economic_snippets(
    released_events
)

        released_events = released_events[
            released_events["actual"].notna()
        ]

        released_events = released_events[
            released_events["actual"] != ""
        ]

        released_events = released_events.tail(5)

        if not released_events.empty:

            released_events["actual"] = (
                released_events["actual"]
                .fillna("")
            )

            released_events["forecast"] = (
                released_events["forecast"]
                .fillna("")
            )

        # Upcoming events

        upcoming_events = economic_calendar.copy()

        upcoming_events = upcoming_events[
            upcoming_events["impact"] == "High"
        ]

        upcoming_events = upcoming_events.head(4)

        upcoming_events["forecast"] = (
            upcoming_events["forecast"]
            .fillna("")
        )

        upcoming_events["date"] = pd.to_datetime(
            upcoming_events["date"]
        )

        upcoming_events["date"] = (
            upcoming_events["date"]
            .dt.strftime("%d %b | %H:%M")
        )

        upcoming_events["display_event"] = (
            upcoming_events.apply(
                lambda x:
                f"{x['title']} (Cons: {x['forecast']})"
                if str(x["forecast"]).strip() != ""
                else x["title"],
                axis=1
            )
        )

    commentary = generate_commentary(
    indian_markets,
    global_markets,
    commodities
)
    corporate_news = fetch_corporate_news()

    print("Loading HTML template...")

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "report_template.html"
    )

    print("Rendering dashboard...")

    html = template.render(

        commentary=commentary,

        corporate_news=corporate_news,
        bulk_deals=bulk_deals,
        economic_snippets=economic_snippets,

        indian_markets=indian_markets.to_dict(
            orient="records"
        ),

        global_markets=global_markets.to_dict(
            orient="records"
        ),

        commodities=commodities.to_dict(
            orient="records"
        ),

        fxgsec=fxgsec.to_dict(
            orient="records"
        ),

        gainers=gainers.to_dict(
            orient="records"
        ),

        losers=losers.to_dict(
            orient="records"
        ),

        economic_data=economic_data.to_dict(
            orient="records"
        ),

        released_events=released_events.to_dict(
            orient="records"
        ),

        upcoming_events=upcoming_events.to_dict(
            orient="records"
        ),

        participants=participants.to_dict(
            orient="records"
        )

    )

    with open(
        "daily_report.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("Dashboard generated successfully!")

    return html


if __name__ == "__main__":

    generate_dashboard()