# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import yfinance as yf
import pandas as pd
import datetime

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

US_BUSINESS_DAY = CustomBusinessDay(calendar=USFederalHolidayCalendar())

# from exportToFirebase import addTable

# import time
# from util.stat import compute_rs_rating

yf.pdr_override()

# # Variables
# # Tickers get
# tickers = si.tickers_nasdaq()
# tickers = [
#     item.replace(".", "-") for item in tickers
# ]  # Yahoo Finance uses dashes instead of dots

# # # Save list to csv
# data = pd.read_csv("./america_2022-03-05.csv", header=0)
# tickers = [
#     item.replace(".", "-") for item in data.Ticker
# ]  # Yahoo Finance uses dashes instead of dots
# dict = {"Symbol": tickers, "Sector": data.Sector, "Industry": data.Industry}
# df = pd.DataFrame(dict)
# df.to_csv("./tickers_above10-03-05a.csv")

data = pd.read_csv("./tickers_above231002.csv", header=0)
tickers = list(data.Symbol)

index_name = "^GSPC"  # S&P 500
start_date = datetime.datetime.now() - datetime.timedelta(days=120)
end_date = datetime.date.today()


# def getReturnMultiple(df, index_return):
#     df["Percent Change"] = df["Adj Close"].pct_change()
#     stock_return = (df["Percent Change"] + 1).cumprod()[-1]

#     returns_multiple = round((stock_return / index_return), 2)
#     returns_multiples.extend([returns_multiple])

#     # add extra column
#     industries.extend([row.Industry])
#     latestPercentageChange = (df["Percent Change"].iloc[-1] * 100).round(2)
#     latestPercentageChanges.extend([latestPercentageChange])


def run(firstRun=False):
    exportList = pd.DataFrame(
        columns=[
            "Stock",
            "RS_Rating",
            "50 Day MA",
            "150 Day MA",
            "200 Day MA",
            "52 Week Low",
            "52 Week High",
            "Industry",
            "Daily_change",
            "returnsMultiple",
        ]
    )
    returns_multiples = []
    industries = []
    latestPercentageChanges = []
    skip_days = 80

    # Index Returns
    if firstRun:
        index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
        index_df.to_csv("stocks/a_spy.csv")
    else:
        index_df = pd.read_csv("stocks/a_spy.csv", index_col=0)
        # index_df = pd.read_csv(
        #     "stocks/a_spy.csv", index_col=0, skiprows=range(2, skip_days)
        # )
    index_df["Percent Change"] = index_df["Adj Close"].pct_change()
    index_return = (index_df["Percent Change"] + 1).cumprod()[-1]
    print(111, index_df)

    latest_date = ""

    # Find top 30% performing stocks (relative to the S&P 500)
    for index, row in data.iterrows():
        # Download historical data as CSV for each stock (makes the process faster)
        if firstRun:
            df = pdr.get_data_yahoo(row["Symbol"], start_date, end_date)
            df.to_csv(f"stocks/{row['Symbol']}.csv")
        else:
            # df = pd.read_csv(
            #     f"stocks/{row['Symbol']}.csv", index_col=0, skiprows=range(2, skip_days)
            # )
            df = pd.read_csv(f"stocks/{row['Symbol']}.csv", index_col=0)

        # if row["Symbol"] == "AAPL":
        #     latest_date = df.index[-1]

        # Calculating returns relative to the market (returns multiple)
        df["Percent Change"] = df["Adj Close"].pct_change()
        stock_return = (df["Percent Change"] + 1).cumprod()[-1]
        print(stock_return)

        returns_multiple = round((stock_return / index_return), 2)
        returns_multiples.extend([returns_multiple])

        # add extra column
        industries.extend([row.Industry])
        latestPercentageChange = (df["Percent Change"].iloc[-1] * 100).round(2)
        latestPercentageChanges.extend([latestPercentageChange])
        # data = compute_rs_rating(df)
        # if data:
        #     print(9, data.get("rs1"), data.get("rs2"))

        print(f"Ticker: {row.Symbol};")
        print("Returns Multiple against S&P 500: {returns_multiple}\n")
        # time.sleep(1)

    # Creating dataframe of only top 30%
    rs_df = pd.DataFrame(
        list(
            zip(
                tickers,
                returns_multiples,
                industries,
                latestPercentageChanges,
            )
        ),
        columns=[
            "Ticker",
            "Returns_multiple",
            "Industry",
            "Daily_change",
        ],
    )
    rs_df["Returns_multiple"] = rs_df.Returns_multiple
    rs_df["RS_Rating"] = rs_df.Returns_multiple.rank(pct=True) * 100
    if not firstRun:
        rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(0.70)]

    # Checking Minervini conditions of top 30% of stocks in given list
    rs_stocks = rs_df["Ticker"]
    for stock in rs_stocks:
        try:
            df = pd.read_csv(f"stocks/{stock}.csv", index_col=0)
            sma = [50, 150, 200]
            for x in sma:
                df["SMA_" + str(x)] = round(df["Adj Close"].rolling(window=x).mean(), 2)

            # Storing required values
            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = round(min(df["Low"][-260:]), 2)
            high_of_52week = round(max(df["High"][-260:]), 2)
            RS_Rating = round(rs_df[rs_df["Ticker"] == stock].RS_Rating.tolist()[0])
            Industry = rs_df[rs_df["Ticker"] == stock].Industry.tolist()[0]
            Daily_change = rs_df[rs_df["Ticker"] == stock].Daily_change.tolist()[0]
            returnsMultiple = rs_df[rs_df["Ticker"] == stock].Returns_multiple.tolist()[
                0
            ]

            try:
                moving_average_200_20 = df["SMA_200"][-20]
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            condition_1 = currentClose > moving_average_150 > moving_average_200

            # Condition 2: 150 SMA and > 200 SMA
            condition_2 = moving_average_150 > moving_average_200

            # Condition 3: 200 SMA trending up for at least 1 month
            condition_3 = moving_average_200 > moving_average_200_20

            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            condition_4 = moving_average_50 > moving_average_150 > moving_average_200

            # Condition 5: Current Price > 50 SMA
            condition_5 = currentClose > moving_average_50

            # Condition 6: Current Price is at least 30% above 52 week low
            condition_6 = currentClose >= (1.3 * low_of_52week)

            # Condition 7: Current Price is within 25% of 52 week high
            condition_7 = currentClose >= (0.75 * high_of_52week)

            # Condition 8: Current Price is within 25% of 52 week high
            condition_8 = currentClose >= (0.70 * high_of_52week)

            # If all conditions above are true, add stock to exportList
            conditions = (
                condition_1
                and condition_2
                and condition_3
                and condition_4
                and condition_5
                and condition_6
                and condition_7
            )
            if firstRun:
                conditions = condition_8
            if conditions:
                exportList = exportList.append(
                    {
                        "Stock": stock,
                        "RS_Rating": RS_Rating,
                        "50 Day MA": moving_average_50,
                        "150 Day MA": moving_average_150,
                        "200 Day MA": moving_average_200,
                        "52 Week Low": low_of_52week,
                        "52 Week High": high_of_52week,
                        "Industry": Industry,
                        "Daily_change": Daily_change,
                        "returnsMultiple": returnsMultiple,
                    },
                    ignore_index=True,
                )
                print(stock + " made the Minervini requirements")
        except Exception as e:
            print(e)
            print(f"Could not gather data on {stock}")

    exportList = exportList.sort_values(by="RS_Rating", ascending=False)
    # if not firstRun:
    #     addTable("table_us", exportList, latest_date)
    exportList.to_csv("ScreenOutput.csv")
    print("\n", exportList)


run(True)
