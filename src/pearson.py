"""
Calculate the Pearson Linearity score for a given input
"""

import pandas as pd
from scipy.stats import pearsonr
from tqdm import tqdm
import numpy as np

# Get dataframe from DB
# DB = "C:/Users/eirik/Codebase/Database/"
DB = "../Database/"

def pearson_ranker_old(tickerlist:list, metric):

    # Call & Create variables
    df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
    fails = 0
    list_pearson = []

    # Loop through elements in the input list
    # PERF: Not optimized. Write to multithread
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


def pearson_ranker(tickerlist:list, metric):

    # Call & Create variables
    df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
    fails = 0
    list_pearson = []
    
    groups = df_metric.groupby(df_metric['ticker'])

    for i in tqdm(range(len(tickerlist))):
        ticker = tickerlist[i]
        try:
            group = groups.get_group(ticker)
            x = group.index.to_numpy()
            y = group[f'ttm {metric}']

            df_pearson_single = (
                [[ticker,
                metric,
                np.corrcoef(x,y)[0,1],
                len(x)]]
            )

        except:
            fails += 1
            df_pearson_single = (
                [[ticker,
                metric,
                0,
                0]]
            )

        df_pearson = (
            pd.DataFrame(
                df_pearson_single,
                columns = ["ticker","metric","pearson r","pearson quarters"]
            )
        )
        list_pearson.append(df_pearson)
     
    return list_pearson, fails
