from datafetcher import fetch_indices_data
from analytics import fetch_top_movers
from economic_calendar_scraper import get_calendar
from dashbodard_generator import generate_dashboard
from email_sender import send_email
from corporate_news_fetcher import fetch_corporate_news
from bulk_deals_fetcher import fetch_bulk_deals


def run_pipeline():

    corporate_news = fetch_corporate_news()

    bulk_deals = fetch_bulk_deals()

    print(
        f"Corporate News: {len(corporate_news)}"
    )

    print(
        f"Bulk Deals: {len(bulk_deals)}"
    )

    print("Fetching market data...")
    fetch_indices_data()

    print("Running analytics...")
    fetch_top_movers()

    print("Fetching economic calendar...")

    calendar_df = get_calendar()

    calendar_df.to_csv(
        "economic_calendar_dashboard.csv",
        index=False
    )

    print("Generating dashboard...")

    html = generate_dashboard()

    print("Sending email...")

    send_email(html)

    print("Pipeline completed.")


if __name__ == "__main__":
    run_pipeline()