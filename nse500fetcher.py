import pandas as pd

url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"

df = pd.read_csv(url)

df = df[[
    "Symbol",
    "Company Name",
    "Industry"
]]

df.columns = [
    "symbol",
    "company_name",
    "sector"
]

df["symbol"] = df["symbol"] + ".NS"

df.to_csv("stocks.csv", index=False)

print("NSE 500 stock list created successfully!")