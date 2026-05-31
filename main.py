from datafetcher import fetch_indices_data
from analytics import fetch_top_movers
from dashbodard_generator import generate_dashboard
from email_sender import send_email


def run_pipeline():

    print("Fetching market data...")
    fetch_indices_data()

    print("Running analytics...")
    fetch_top_movers()

    print("Generating dashboard...")
    html = generate_dashboard()

    print("Sending email...")
    send_email(html)

    print("Pipeline completed.")


if __name__ == "__main__":
    run_pipeline()