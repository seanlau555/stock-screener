# Imports
import pandas as pd
from exportToFirebase import addIndustryTable

df = pd.read_csv("./ScreenOutput.csv")


gkk = df.groupby("Industry")

df = pd.read_csv("stocks/A.csv", index_col=0)
latest_date = df.index[0]

gkk = gkk.mean()
addIndustryTable("industry_sum", gkk, latest_date)

gkk = gkk.sort_values(by="Daily_change", ascending=False)
re = gkk.Daily_change
re.to_csv("ScreenOutputDailyGroup.csv")

gkk = gkk.sort_values(by="RS_Rating", ascending=False)
re = gkk.RS_Rating
re.to_csv("ScreenOutputRSGroup.csv")
