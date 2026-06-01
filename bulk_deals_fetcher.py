import requests
from datetime import datetime, timedelta


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}


def fetch_bulk_deals():

    today = datetime.today()
    week_ago = today - timedelta(days=7)

    from_date = week_ago.strftime("%d-%m-%Y")
    to_date = today.strftime("%d-%m-%Y")

    url = (
        "https://www.nseindia.com/api/"
        "historicalOR/bulk-block-short-deals"
        f"?optionType=bulk_deals"
        f"&from={from_date}"
        f"&to={to_date}"
    )

    session = requests.Session()
    session.headers.update(HEADERS)

    # NSE cookie handshake
    session.get(
        "https://www.nseindia.com",
        timeout=15
    )

    response = session.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    records = data["data"]

    deals = []

    for row in records[:15]:

        deals.append({

            "date":
                row.get(
                    "BD_DT_DATE",
                    ""
                ),

            "symbol":
                row.get(
                    "BD_SYMBOL",
                    ""
                ),

            "company":
                row.get(
                    "BD_SCRIP_NAME",
                    ""
                ),

            "client":
                row.get(
                    "BD_CLIENT_NAME",
                    ""
                ),

            "action":
                row.get(
                    "BD_BUY_SELL",
                    ""
                ),

            "quantity":
                row.get(
                    "BD_QTY_TRD",
                    0
                ),

            "price":
                row.get(
                    "BD_TP_WATP",
                    0
                )

        })

    return deals


if __name__ == "__main__":

    deals = fetch_bulk_deals()

    print(
        f"Fetched {len(deals)} deals\n"
    )

    for d in deals:

        print(
            f"{d['date']} | "
            f"{d['symbol']} | "
            f"{d['client']} | "
            f"{d['action']} | "
            f"{d['quantity']:,} | "
            f"₹{d['price']}"
        )