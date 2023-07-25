


import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def scrape_mt(link):

    dict_items = {}
    html = requests.get(link, timeout = 10, headers = header)
    soup = BeautifulSoup(html.text, 'html.parser')
    htmltext = soup.prettify()

    items = htmltext.split("var ")[1:]
    for i in items:
        name = i.split("=")[0].strip()
        try:
            value = i.split("originalData =")[1]
            value = value.replace(';','')
        
        except: 
            value = 0

        dict_items[name] = value

    data = dict_items["originalData"]

    # Formatting
    data = json.loads(data)
    df_data = pd.DataFrame.from_dict(data)

    df_data["field_name"] = df_data["field_name"].str.split(">").str[1]
    df_data["field_name"] = df_data["field_name"].str.split("<").str[0]
    df_data = df_data.drop(["popup_icon"], axis = 1)
    df_data = df_data.rename(columns = {'field_name':'Date'})
    df_data.index = df_data["Date"]
    df_data = df_data.drop(["Date"], axis = 1)
    df_data = df_data.T
    df_data = df_data.reset_index()
    df_data = df_data.rename(columns = {'index':'Date'})
    df_data = df_data.sort_values(by=["Date"])

    return df_data
