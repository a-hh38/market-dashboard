import yfinance as yf
import pandas as pd
from database import engine

stocks_df = pd.read_csv("stocks.csv")

stock_list = stocks_df["symbol"].tolist()


def fetch_top_movers():

    movers = []

    print("Downloading NSE500 market data...")

    try:

        data = yf.download(
            tickers=stock_list,
            period="2d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False
        )

    except Exception as e:
        print(f"Download failed: {e}")
        return None, None

    for stock in stock_list:

        try:

            stock_data = data[stock]

            if stock_data.empty:
                continue

            close_latest = stock_data["Close"].iloc[-1].item()

            close_previous = stock_data["Close"].iloc[-2].item()

            percent_change = (
                (close_latest - close_previous)
                / close_previous
            ) * 100

            company_name = stocks_df.loc[
                stocks_df["symbol"] == stock,
                "company_name"
            ].values[0]

            sector = stocks_df.loc[
                stocks_df["symbol"] == stock,
                "sector"
            ].values[0]

            movers.append({

                "company_name": company_name,

                "sector": sector,

                "closing_price": round(
                    close_latest,
                    2
                ),

                "rate_change": round(
                    percent_change,
                    2
                )

            })

        except Exception as e:
            print(f"Error processing {stock}: {e}")

    df = pd.DataFrame(movers)

    if df.empty:
        print("No movers generated.")
        return

    gainers = df.sort_values(
        by="rate_change",
        ascending=False
    ).head(10)

    losers = df.sort_values(
        by="rate_change",
        ascending=True
    ).head(10)

    gainers.to_sql(
        "top_gainers",
        engine,
        if_exists="replace",
        index=False
    )

    losers.to_sql(
        "top_losers",
        engine,
        if_exists="replace",
        index=False
    )

    print("Top movers generated successfully!")