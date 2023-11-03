import pandas as pd

# # Save list to csv
data = pd.read_csv("./20231103.csv", header=0)
symbols = [
    item.replace(".", "-") for item in data.Symbol
]  # Yahoo Finance uses dashes instead of dots
dict = {"Symbol": symbols, "Industry": data.Industry}
df = pd.DataFrame(dict)
df.to_csv("./tickers_above231103.csv")


# import csv
# import json


# # Function to convert a CSV to JSON
# # Takes the file paths as arguments
# def make_json(csvFilePath, jsonFilePath):

#     # create a dictionary
#     data = []

#     # Open a csv reader called DictReader
#     with open(csvFilePath, encoding="utf-8") as csvf:
#         csvReader = csv.DictReader(csvf)

#         # Convert each row into a dictionary
#         # and add it to data
#         for rows in csvReader:

#             # Assuming a column named 'No' to
#             # be the primary key
#             # key = rows["Index"]
#             # data[key] = rows
#             data.append(rows)

#     # Open a json writer, and use the json.dumps()
#     # function to dump data
#     with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
#         jsonf.write(json.dumps(data, indent=4))


# # Call the make_json function
# make_json("./ScreenOutput.csv", "ScreenOutput.json")
# # # # Convert to JSON
# # df = pd.read_csv("./ScreenOutput.csv", header=0)
# # df.to_json("ScreenOutput.json")
