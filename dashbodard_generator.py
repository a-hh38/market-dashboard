from jinja2 import Environment, FileSystemLoader
import pandas as pd

from database import engine


def generate_dashboard():

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

    # Economic Data
    try:

        economic_data = pd.read_csv(
            "economic_data.csv"
        )

    except:

        economic_data = pd.DataFrame()

    # Participants Activity
    try:

        participants = pd.read_csv(
            "participants_activity.csv"
        )

    except:

        participants = pd.DataFrame()

    # Static Commentary
    commentary = """

    Dow Jones traded weak overnight amid persistent concerns surrounding global growth and elevated interest rates. Investors continued to monitor commentary from major central bank officials while commodity prices remained volatile across global markets.

    Indian equities witnessed selective buying interest led by financials and industrials, although broader market sustainability continues to remain dependent on global risk appetite and evolving macroeconomic conditions.

    """

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