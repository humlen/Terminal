"""
Calculate the Kendall Tau score for a given input
"""

import pandas as pd 
from scipy.stats import kendalltau
from tqdm import tqdm 


# DB = "C:/Users/eirik/Codebase/Database/"
DB = "../Database/"

def kendall_ranker(tickerlist:list, metric):
    
    # Call & Create variables
    df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
    fails = 0
    list_kendall = []

    groups = df_metric.groupby(df_metric['ticker'])

    for i in tqdm(range(len(tickerlist))):
        ticker = tickerlist[i]
        
        try:
            group = groups.get_group(ticker)
            x = group.index.to_numpy()
            y = group[f'ttm {metric}']
            
            df_kendall_single = (
                [[ticker,
                metric,
                kendalltau(x,y).statistic,
                len(x)]]
            )

        except:
            fails += 1 
            df_kendall_single = (
                [[ticker,
                metric,
                0,
                0]]
            )

        df_kendall = (
            pd.DataFrame(
                df_kendall_single,
                columns = ['ticker','metric','kendall tau','kendall quarters']
            )
        )

        list_kendall.append(df_kendall)

    return list_kendall, fails
