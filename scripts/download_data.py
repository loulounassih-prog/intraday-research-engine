from intraday_research_engine.data.download import download_price_data


if __name__ == "__main__":
    file_path = download_price_data(
        ticker="SPY",
        start="2020-01-01",
        end="2024-01-01",
        interval="1d",
    )

    print(f"Data saved to: {file_path}")