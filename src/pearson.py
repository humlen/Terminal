"""
Calculate the Pearson Linearity score for a given input
"""

import pandas as pd
from scipy.stats import pearsonr
from tqdm import tqdm

# Get dataframe from DB
DB = "C:/Users/eirik/OneDrive/Documents/Cloudkit/Database/"

def pearson_ranker(tickerlist:list, metric):

    # Call & Create variables
    df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
    fails = 0
    list_pearson = []

    # Loop through elements in the input list
    for i in tqdm(range(len(tickerlist))):
        ticker = tickerlist[i]

        try:
            # Attempt to calculate pearson r for the metric
            dataframe = df_metric[(df_metric["ticker"] == ticker)]
            dataframe.reset_index(drop=True, inplace = True)
            df_pearson_single =(
                [[ticker,
                metric,
                pearsonr(
                    dataframe.index,
                    dataframe[f"ttm {metric}"]
                    ).statistic, # type: ignore
                max(dataframe.index)+1]]
            )

        except:
            # If it fails, increment failure counter
            df_pearson_single = (
                [[ticker,
                metric,
                0,
                0]]
            )
            fails += 1

        # Append the resulting dataframe to a list
        df_pearson =(
            pd.DataFrame(
                df_pearson_single, # type: ignore
                columns = ["ticker","metric","pearson r","pearson quarters"] 
            )
        )

        list_pearson.append(df_pearson)

    return list_pearson, fails

