import yfinance as yf
import pandas as pd
from database import engine

market_indices = {

    # Indian Markets
    "Nifty": "^NSEI",
    "Sensex": "^BSESN",
    "BSE Small Cap": "^BSESML",
    "Midcap": "^NSEMDCP50",
    "USD/INR": "INR=X",

    # Developed / Emerging Markets
    "Dow Jones": "^DJI",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Nikkei": "^N225",
    "Hang Seng": "^HSI",
    "Bovespa": "^BVSP",
    "DAX": "^GDAXI",
    "FTSE": "^FTSE",
    "SGX Nifty": "^SGXNIFTY"
}

commodities = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F",
    "Aluminium": "ALI=F",
    "Zinc": "ZNC=F",
    "Lead": "PBL=F",
    "Nickel": "NICKEL=F",
    "Br. Crude": "BZ=F"
}

fx_gsec = {
    "USD/INR": "INR=X",
    "EUR/USD": "EURUSD=X",
    "US 10YR": "^TNX",
    "India 10YR": "^INDIAGOVT10Y"
}


def calculate_changes(close_prices):

    latest = close_prices.iloc[-1].item()

    def pct_change(current, previous):
        return round(((current - previous) / previous) * 100, 1)

    return {
        "last_price": round(latest, 2),

        "change_1d": pct_change(
            latest,
            close_prices.iloc[-2].item()
        ),

        "change_3m": pct_change(
            latest,
            close_prices.iloc[-63].item()
        ),

        "change_6m": pct_change(
            latest,
            close_prices.iloc[-126].item()
        ),

        "change_1y": pct_change(
            latest,
            close_prices.iloc[0].item()
        )
    }


def process_market_group(group_dict):

    rows = []

    for name, ticker in group_dict.items():

        try:

            data = yf.download(
                ticker,
                period="1y",
                interval="1d",
                progress=False
            )

            if data.empty:
                continue

            close_prices = data["Close"].dropna()

            metrics = calculate_changes(close_prices)

            row = {
                "market": name,
                **metrics
            }

            rows.append(row)

            print(f"{name} fetched successfully")

        except Exception as e:
            print(f"Error fetching {name}: {e}")

    return pd.DataFrame(rows)


def fetch_indices_data():

    print("Fetching Indian markets...")
    indian_markets = process_market_group(
        dict(list(market_indices.items())[:5])
    )

    print("Fetching global markets...")
    global_markets = process_market_group(
        dict(list(market_indices.items())[5:])
    )

    print("Fetching commodities...")
    commodities_df = process_market_group(
        commodities
    )

    print("Fetching FX & G-Sec...")
    fxgsec_df = process_market_group(
        fx_gsec
    )

    indian_markets.to_sql(
        "indian_markets",
        engine,
        if_exists="replace",
        index=False
    )

    global_markets.to_sql(
        "global_markets",
        engine,
        if_exists="replace",
        index=False
    )

    commodities_df.to_sql(
        "commodities",
        engine,
        if_exists="replace",
        index=False
    )

    fxgsec_df.to_sql(
        "fxgsec",
        engine,
        if_exists="replace",
        index=False
    )

    print("All market datasets stored successfully!")