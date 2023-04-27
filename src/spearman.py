"""
Calculate the spearman Linearity score for a given input
"""

import pandas as pd
from scipy.stats import spearmanr
from tqdm import tqdm

# Get dataframe from DB
DB = "C:/Users/eirik/Codebase/Database/"

def spearman_ranker(tickerlist:list, metric):

    # Call & Create variables
    df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
    fails = 0
    list_spearman = []

    # Loop through elements in the input list
    for i in tqdm(range(len(tickerlist))):
        ticker = tickerlist[i]

        try:
            # Attempt to calculate spearman r for the metric
            dataframe = df_metric[(df_metric["ticker"] == ticker)]
            dataframe.reset_index(drop=True, inplace = True)
            df_spearman_single =(
                [[ticker,
                metric,
                spearmanr(
                    dataframe.index,
                    dataframe[f"ttm {metric}"]
                    ).statistic, # type: ignore
                max(dataframe.index)+1]]
            )

        except:
            # If it fails, increment failure counter
            fails += 1
            df_spearman_single = (
                    [[ticker,
                    metric,
                    0,
                    0]]
            )

        # Append the resulting dataframe to a list
        df_spearman=(
            pd.DataFrame(
                df_spearman_single, # type: ignore
                columns = ["ticker","metric","spearman r","spearman quarters"] 
            )
        )

        list_spearman.append(df_spearman)

    return list_spearman, fails

