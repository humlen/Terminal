import numpy as np
from tqdm import tqdm
import pandas as pd
from pearson import pearson_ranker

DB = 'C:/Users/eirik/codebase/database/'
metric = 'revenue'
tickerlist = ['MSFT','AAPL']

df_metric = pd.read_csv(f"{DB}master__{metric}.csv")
fails = 0
list_pearson = []

groups = df_metric.groupby(df_metric['ticker'])

for i in tqdm(range(len(tickerlist))):
    ticker = tickerlist[i]
    group = groups.get_group(ticker)
    x = group.index.to_numpy()
    y = group[f'ttm {metric}']

    pearson = np.corrcoef(x,y)[0,1]
    df_pearson_single = (
        [[ticker,
        metric,
        np.corrcoef(x,y)[0,1],
        len(x)]]
    )


    df_pearson = (
        pd.DataFrame(
            df_pearson_single,
            columns = ["ticker","metric","pearson r","pearson quarters"]
        )
    )
    list_pearson.append(df_pearson)
    
print(list_pearson)


var1, var2 = pearson_ranker(tickerlist,'revenue')

print(var1)
