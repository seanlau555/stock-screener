import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Fetch the service account key JSON file contents
cred = credentials.Certificate("mon21-32508-firebase-adminsdk-qz22w-131f137f64.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://mon21-32508.firebaseio.com/"}
)

firestore_db = firestore.client()


# now = datetime.now() - timedelta(days=1)
# date = now.strftime("%Y-%m-%d")
# # add data
# firestore_db.collection("table").add({"data": data, "date": date})

# batch add
def addTable(collection_name, exportList, date):
    batch = firestore_db.batch()
    for _, row in exportList.iterrows():
        table_ref = firestore_db.collection(collection_name).document()
        batch.set(
            table_ref,
            {
                "date": date,
                "ticker": row["Stock"],
                "rsRating": row["RS_Rating"],
                "52WeekHigh": row["52 Week High"],
                "52WeekLow": row["52 Week Low"],
                "50DayMa": row["50 Day MA"],
                "150DayMa": row["150 Day MA"],
                "200DayMa": row["200 Day MA"],
                "sector": row["Sector"],
                "industry": row["Industry"],
                "returnsMultiple": row["returnsMultiple"],
                "dailyChange": row["Daily_change"],
            },
        )
    batch.commit()


def addIndustryTable(collection_name, rows, date):
    batch = firestore_db.batch()
    for _, row in rows.iterrows():
        table_ref = firestore_db.collection(collection_name).document()
        batch.set(
            table_ref,
            {
                "date": date,
                # "sector": row["Sector"],
                "industry": row.name,
                "dailyChange": row["Daily_change"],
                "rsRating": row["RS_Rating"],
            },
        )
    batch.commit()


def readTable(collection_name):
    now = datetime.now() - timedelta(days=1)
    date = now.strftime("%Y-%m-%d")
    # read data
    table_ref = firestore_db.collection(collection_name)
    # get latest
    query = table_ref.where("date", "==", date).order_by("rsRating", "DESCENDING")
    docs = query.stream()
    # result = query.get()
    # print(result.to_dict())
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")


# readTable("table_us")
