import pandas as pd
import requests
from pathlib import Path


def get_bonus(symbol: str):
    try:
        html = requests.get(
            f"https://www.nepsealpha.com/ajax/investment_calander/{symbol}"
        ).json()["html"]
        bonus_table = pd.read_html(html)[0]
        latest_bonus = bonus_table.iloc[0, 0].replace(" %", "")
        return latest_bonus
    except Exception:
        return -1


def main():
    (df,) = pd.read_html("https://www.nepsealpha.com/trading-signals/funda/")

    df = df.dropna(how="all")
    df["Undervalued"] = (
        df.loc[:, "PE vs Sector":"ROE Vs Sector"] == "Undervalued"
    ).sum(axis=1)

    df = df.loc[:, ["Symbol", "Ratios Summary", "Sector", "LTP", "Undervalued"]]
    df["Bonus"] = df["Symbol"].apply(get_bonus)
    df["Ratios Summary"] = df["Ratios Summary"].replace(
        {"Strong": 1, "Medium": 0, "Weak": -1}
    )

    df["Symbol"] = df["Symbol"].apply(
        lambda symbol: f"[{symbol}](https://www.nepsealpha.com/stocks/{symbol}/info)"
    )
    df = df.sort_values(
        by=["Undervalued", "Ratios Summary", "LTP", "Bonus"],
        ascending=[False, False, True, False],
    )
    stock_table = df.to_markdown(index=False)
    Path("README.md").write_text(stock_table)


if __name__ == "__main__":
    main()
