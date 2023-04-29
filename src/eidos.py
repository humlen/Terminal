"""
@author: eirik
@date: 2023-01-012

A tool to generate a ranking of companies by the linearity of their earnings results
"""
import time
import warnings

import pandas as pd

from .pearson import pearson_ranker, pearson_ranker_old
from .spearman import spearman_ranker # type: ignore

warnings.filterwarnings("ignore")


# Sets the Product Name and Version variables
__v_name__ = 'Eidos'
__v_number__ = '2.2'

# This ensures that the Eidos display shows correctly in Terminal.py
pd.set_option('display.max_rows', None) # (display all rows)
pd.set_option('display.max_columns', None) # (display all columns)
pd.set_option('display.width', 1000)

# Start of program
print("Booting "+__v_name__+" v "+__v_number__+"...")\

# Databases
DB = "C:/Users/eirik/Codebase/Database/"

# ticker Data
df_tickers = pd.read_csv(f"{DB}master__tickers.csv")

def eidos_revenue():
    """This script will rank the linearity of all companies'
    revenue, and assign the linearity a sector-adusted score"""

    # Start your engines
    start_time = time.time()
 
    # Get Unique data
    dataset_revenue = pd.read_csv(f"{DB}master__revenue.csv")
    tickerlist = dataset_revenue["ticker"].unique().tolist()

    # new method
    print("\nCalculating Pearson linearity")
    pearson_list, pearson_fails = pearson_ranker(tickerlist,'revenue')    
    print("\nCalculating Spearman linearity")
    spearman_list, spearman_fails = spearman_ranker(tickerlist, 'revenue')

    # Concatenate dataframes
    df_spearman_revenue = pd.concat(spearman_list, axis = 0)
    df_pearson_revenue = pd.concat(pearson_list, axis = 0)

    # Create Scoresheet
    df_eidos = df_tickers.merge(
        df_spearman_revenue,
        how="left", left_on="ticker", right_on="ticker", suffixes=("_Spearman", "")
        )
    df_eidos = df_eidos.merge(
        df_pearson_revenue, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Pearson", "")
    )
    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc",
                  "pearson r", "pearson quarters", "spearman r", "spearman quarters"
                ]]
    )
    df_eidos = df_eidos.loc[
        (df_eidos["spearman quarters"] > 20)
    ]
    df_eidos["Score"] = (
        round(df_eidos["pearson r"] * df_eidos["spearman r"] * 100,2))
   
    # Retain only the important columns
    df_eidos = (
        df_eidos.rename(
        columns = {"comp_name_2":"Company","sector":"Sector","zacks_x_ind_desc":"Industry"})
        .reset_index(drop=True)
    )

    # Calculate mean of each sector
    df_eidos["Sector Mean"] = (
        df_eidos.groupby(["Sector"])["Score"].transform('mean')
    )
    
    # Calculate standard deviation of each sector
    df_eidos["Sector StdDev"] = (
        df_eidos.groupby(["Sector"])["Score"].transform('std')
    )
    
    # Calculate equity deviance from mean
    df_eidos["Sector-Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Create subset with deviation greater than 1
    df_gold_revenue = (
        df_eidos[df_eidos["Sector-Adj. Score"] > 1]
        [["ticker", "Company", "Sector", "Industry", "Score","Sector-Adj. Score"]]
    )
    df_gold_revenue = df_gold_revenue.sort_values(by=("Sector-Adj. Score"), ascending = False)

    # Print Output
    print("\n \n We were able to locate " +
    str(len(df_gold_revenue)-1) + " revenue Gold candidates:")
    print(df_gold_revenue)

    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Success Rate: {100*round((len(df_eidos.index)-pearson_fails-spearman_fails)/len(df_eidos.index),2)}%
    Time Elapsed: {round(time.time()-start_time,2)} Seconds
    """)


def eidos_netinc():
    """This script will rank the linearity of all companies'
    net income, and assign the linearity with a sector-adjusted
    score"""

    # Start your engines
    start_time = time.time()

    # Get Unique Data
    dataset_netinc = pd.read_csv(f"{DB}master__netincome.csv")
    tickerlist = dataset_netinc["ticker"].unique().tolist()
   
   # new
    print("\nCalculating Pearson linearity")
    pearson_list, pearson_fails = pearson_ranker(tickerlist,'netincome')    
    print("\nCalculating Spearman linearity")
    spearman_list, spearman_fails = spearman_ranker(tickerlist, 'netincome')

    # Concatenate dataframes
    df_spearman_netinc = pd.concat(spearman_list, axis = 0)
    df_pearson_netinc = pd.concat(pearson_list, axis = 0)

    # Create Scoresheet
    df_eidos = df_tickers.merge(
        df_spearman_netinc, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Spearman", "")
    )
    df_eidos = df_eidos.merge(
        df_pearson_netinc, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Pearson", "")
    )
    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc","pearson r",\
                   "pearson quarters", "spearman r", "spearman quarters"]]
    )

    df_eidos = df_eidos.loc[
        (df_eidos["spearman quarters"] > 20)
    ]
    df_eidos["Score"] = round(df_eidos["pearson r"] * df_eidos["spearman r"] * 100,2)
    df_eidos = df_eidos.sort_values(by=("Score"), ascending = False)
    df_eidos = (
        df_eidos
        .rename(columns = {"comp_name_2":"Company","sector":"Sector","zacks_x_ind_desc":"Industry"})
        .reset_index(drop=True)
    )

    # Calculate the mean of each sector
    df_eidos["Sector Mean"] = (
        df_eidos.groupby(["Sector"])["Score"].transform('mean')
    ) 
    # Calculate the standard deviation of each sector
    df_eidos["Sector StdDev"] = (
        df_eidos.groupby(["Sector"])["Score"].transform('std')
    )

    # Calculate equity deviance from the mean
    df_eidos["Sector-Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Create subset with the deviation greater than 1
    df_gold_netinc = (
        df_eidos[df_eidos["Sector-Adj. Score"] > 1]
        [["ticker", "Company", "Sector", "Industry", "Score","Sector-Adj. Score"]]
    )
    df_gold_netinc = df_gold_netinc.sort_values(by=("Sector-Adj. Score"), ascending = False)

    # Print Output
    print("\nWe were able to locate " + 
    str(len(df_gold_netinc)-1) + " Net Income Gold candidates:")
    print(df_gold_netinc)

    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Success Rate: {100*round((len(df_eidos.index)-pearson_fails-spearman_fails)/len(df_eidos.index),2)}%
    Time Elapsed: {round(time.time()-start_time,2)} Seconds
    """)


def eidos_eps():
    """This script will rank the linearity of all companies'
    Earnings per Share, and assign the linearity through a 
    sector-adjusted score"""

    # Start your engines
    start_time = time.time()

    # Get Unique Data
    dataset_eps = pd.read_csv(f"{DB}master__eps.csv")
    tickerlist = dataset_eps["ticker"].unique().tolist()

    # new
    print("\nCalculating Pearson linearity")
    pearson_list, pearson_fails = pearson_ranker(tickerlist,'eps')    
    print("\nCalculating Spearman linearity")
    spearman_list, spearman_fails = spearman_ranker(tickerlist, 'eps')
    
    # Concatenate dataframes
    df_spearman_eps = pd.concat(spearman_list, axis = 0)
    df_pearson_eps = pd.concat(pearson_list, axis = 0)

    # Create Scoresheet
    df_eidos = df_tickers.merge(
        df_spearman_eps, how="left", left_on="ticker", right_on="ticker", suffixes=("_Spearman", "")
    )
    df_eidos = df_eidos.merge(
        df_pearson_eps, how="left", left_on="ticker", right_on="ticker", suffixes=("_Pearson", "")
    )
    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc", "pearson r",
                "pearson quarters", "spearman r", "spearman quarters"]]
    )

    df_eidos = df_eidos.loc[(df_eidos["spearman quarters"] > 20)]
    df_eidos["Score"] = round(df_eidos["pearson r"] * df_eidos["spearman r"] * 100,2)
    df_eidos = (
        df_eidos
        .rename(columns = {"comp_name_2":"Company","sector":"Sector","zacks_x_ind_desc":"Industry"})
        .reset_index(drop=True)
    )

    # Mean score adjusted for sector
    df_eidos["Sector Mean"] = df_eidos.groupby(["Sector"])["Score"].transform('mean')
   
   # Standard deviation adjusted for sector
    df_eidos["Sector StdDev"] = df_eidos.groupby(["Sector"])["Score"].transform('std')
   
   # Calculate standard deviations above or below sector mean
    df_eidos["Sector-Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Selects the candidates with scores more than 1 standard deviation above the mean
    # and labels them "Gold" category
    df_gold_eps = (
        df_eidos[df_eidos["Sector-Adj. Score"] > 1]
        [["ticker", "Company", "Sector", "Industry", "Score","Sector-Adj. Score"]]
    )
    df_gold_eps = df_gold_eps.sort_values(by=("Sector-Adj. Score"), ascending = False)

    # Print Output
    print("\n \n We were able to locate " + str(len(df_gold_eps)-1) + " EPS Gold candidates:")
    print(df_gold_eps)

    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Success Rate: {100*round((len(df_eidos.index)-pearson_fails-spearman_fails)/len(df_eidos.index),2)}%
    Time Elapsed: {round(time.time()-start_time,2)} Seconds
    """)




def eidos_test():

    
    # Start your engines
    start_time = time.time()

    # Get Unique Data
    dataset_eps = pd.read_csv(f"{DB}master__test.csv")
    tickerlist = dataset_eps["ticker"].tolist()#.unique().tolist()

    # new
    print("\nCalculating Pearson linearity v1")
    pearson_list, pearson_fails = pearson_ranker_old(tickerlist,'revenue')   
    print("\nCalculating Pearson linearity v2")
    pearson_list_2, pearson_fails_2 = pearson_ranker(tickerlist,'revenue')
    
    # Concatenate dataframes
    df_pearson_eps_v1 = pd.concat(pearson_list, axis = 0)
    df_pearson_eps_v2 = pd.concat(pearson_list_2, axis = 0)

    print("Pearson Old")
    print(df_pearson_eps_v1.head(10))
    print("\nPearson New")
    print(df_pearson_eps_v2.head(10))

    print(f"Pearson fails 1: {pearson_fails}") 
    print(f"Pearson fails 2: {pearson_fails_2}")

