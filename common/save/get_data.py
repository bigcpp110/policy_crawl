from pymongo import MongoClient
import pandas as pd
import json

client=MongoClient(host="127.0.0.1",port=27017)
db=client["policy"]

def get_data(col_name):
    col = db[col_name]
    data = pd.DataFrame(list(col.find({}, {"_id": 0})))
    data.drop_duplicates(["url"], inplace=True, keep="last")
    return data

data=get_data("policy")
data.drop_duplicates(["url"],inplace=True)
print(data.info())
writer = pd.ExcelWriter("政策.xlsx", engine='xlsxwriter', options={'strings_to_urls': False})
data.to_excel(writer)
writer.close()