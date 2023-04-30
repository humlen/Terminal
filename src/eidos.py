"""
@author: eirik
@date: 2023-01-012

A tool to generate a ranking of companies by the linearity of their earnings results
"""
import time
import warnings

import pandas as pd

from .kendall import kendall_ranker
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

    # Calculate the three different linearity rankings that we care 
    # about in this program: Pearson's R, Spearmans Rho and Kendall's 
    # Tau.
    print("\nCalculating Pearson's R")
    pearson_list, pearson_fails = pearson_ranker(tickerlist,'revenue')    
    df_pearson_revenue = pd.concat(pearson_list, axis = 0)
    print("\nCalculating Spearman's Rho")
    spearman_list, spearman_fails = spearman_ranker(tickerlist, 'revenue')
    df_spearman_revenue = pd.concat(spearman_list, axis = 0)
    print("\nCalculating Kendall's Tau")
    kendall_list, kendall_fails = kendall_ranker(tickerlist, 'revenue')
    df_kendall_revenue = pd.concat(kendall_list, axis = 0)
    
    # Merge datasets together
    df_eidos = df_tickers.merge(
        df_spearman_revenue,
        how="left", left_on="ticker", right_on="ticker", suffixes=("_Spearman", "")
        )

    df_eidos = df_eidos.merge(
        df_pearson_revenue, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Pearson", "")
        )

    df_eidos = df_eidos.merge(
        df_kendall_revenue, how = 'left', left_on = 'ticker',
        right_on = 'ticker', suffixes = ('_Kendall','')
        )

    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc",
                  "pearson r", "pearson quarters", "spearman r", "spearman quarters",
                  "kendall tau", "kendall quarters"
                ]]
    )

    # Filter only qualified companies
    df_eidos = df_eidos.loc[
        (df_eidos["spearman quarters"] > 20)
    ]
    df_eidos["Score"] = (
        round(df_eidos["pearson r"] * df_eidos["spearman r"] * df_eidos["kendall tau"] *100,2))
   
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
    df_eidos["Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Create subset with deviation greater than 1
    #df_revenue = (
    #    df_eidos[df_eidos["Adj. Score"] > 1]
    #    [["ticker", "Company", "Sector", "Industry", "Score","Adj. Score"]]
    #)
    df_revenue = df_eidos.sort_values(by=("Adj. Score"), ascending = False)

    # Print Output
    print("\n \n We were able to locate " +
    str(len(df_revenue)-1) + " revenue candidates:")
   
    # New method
    sectorlist = df_revenue.Sector.unique()
    
    for sector in sectorlist:
        print(f"{sector}:")
        print(df_revenue[df_revenue["Sector"] == sector][["ticker","Company","Adj. Score"]].head(10))
        print("\n")

    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Missing Kendall Scores: {kendall_fails}
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
    print("\nCalculating Kendall's Tau")
    kendall_list, kendall_fails = kendall_ranker(tickerlist, 'netincome')

    # Concatenate dataframes
    df_spearman_netinc = pd.concat(spearman_list, axis = 0)
    df_pearson_netinc = pd.concat(pearson_list, axis = 0)
    df_kendall_netinc = pd.concat(kendall_list, axis = 0)

    # Create Scoresheet
    df_eidos = df_tickers.merge(
        df_spearman_netinc, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Spearman", "")
    )

    df_eidos = df_eidos.merge(
        df_pearson_netinc, how="left", left_on="ticker",
        right_on="ticker", suffixes=("_Pearson", "")
    )

    df_eidos = df_eidos.merge(
        df_kendall_netinc, how = 'left', left_on = 'ticker',
        right_on = 'ticker', suffixes = ('_Kendall','')
        )
    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc","pearson r",
                   "pearson quarters", "spearman r", "spearman quarters",
                   "kendall tau", "kendall quarters"]]
    )

    df_eidos = df_eidos.loc[
        (df_eidos["spearman quarters"] > 20)
    ]
    df_eidos["Score"] = round(df_eidos["pearson r"] * df_eidos["spearman r"] * df_eidos["kendall tau"] * 100,2)
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
    df_eidos["Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Create subset with the deviation greater than 1
    # df_netinc = (
    #     df_eidos[df_eidos["Adj. Score"] > 1]
    #     [["ticker", "Company", "Sector", "Industry", "Score","Adj. Score"]]
    # )
    df_netinc = df_eidos.sort_values(by=("Adj. Score"), ascending = False)

    # Print Output
    print("\nWe were able to locate " + 
    str(len(df_netinc)-1) + " Net Income candidates:")
    sectorlist = df_netinc.Sector.unique()
    
    for sector in sectorlist:
        print(f"{sector}:")
        print(df_netinc[df_netinc["Sector"] == sector][["ticker","Company","Adj. Score"]].head(10))
        print("\n")


    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Missing Kendall Scores: {kendall_fails}
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
    print("\nCalculating Kendall's Tau")
    kendall_list, kendall_fails = kendall_ranker(tickerlist, 'eps')
    
    # Concatenate dataframes
    df_spearman_eps = pd.concat(spearman_list, axis = 0)
    df_pearson_eps = pd.concat(pearson_list, axis = 0)
    df_kendall_eps = pd.concat(kendall_list, axis = 0)

    # Create Scoresheet
    df_eidos = df_tickers.merge(
        df_spearman_eps, how="left", left_on="ticker", right_on="ticker", suffixes=("_Spearman", "")
    )

    df_eidos = df_eidos.merge(
        df_pearson_eps, how="left", left_on="ticker", right_on="ticker", suffixes=("_Pearson", "")
    )

    df_eidos = df_eidos.merge(
        df_kendall_eps, how = 'left', left_on = 'ticker',
        right_on = 'ticker', suffixes = ('_Kendall','')
        )

    df_eidos = (
        df_eidos[["ticker", "comp_name_2", "sector", "zacks_x_ind_desc", "pearson r",
                "pearson quarters", "spearman r", "spearman quarters", "kendall tau",
                "kendall quarters"]]
    )

    df_eidos = df_eidos.loc[(df_eidos["spearman quarters"] > 20)]
    df_eidos["Score"] = round(df_eidos["pearson r"] * df_eidos["spearman r"] * df_eidos["kendall tau"] * 100,2)
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
    df_eidos["Adj. Score"] = (
        (df_eidos["Score"]-df_eidos["Sector Mean"])/df_eidos["Sector StdDev"]
    )

    # Selects the candidates with scores more than 1 standard deviation above the mean
    # and labels them top category
    # df_eps = (
    #     df_eidos[df_eidos["Adj. Score"] > 1]
    #     [["ticker", "Company", "Sector", "Industry", "Score","Adj. Score"]]
    # )
    df_eps = df_eidos.sort_values(by=("Adj. Score"), ascending = False)

    # Print Output
    print("\n \n We were able to locate " + str(len(df_eps)-1) + " EPS candidates:")
    #print(df_eps)
    sectorlist = df_eps.Sector.unique()
    
    for sector in sectorlist:
        print(f"{sector}:")
        print(df_eps[df_eps["Sector"] == sector][["ticker","Company","Adj. Score"]].reset_index(drop = True).head(10))
        print("\n")


    # Diagnostics
    print(f"""\nDiagnostics:
    Total Equities Ranked: {len(df_eidos.index)}
    Missing Pearson Scores: {pearson_fails}
    Missing Spearman Scores: {spearman_fails}
    Missing Kendall Scores: {kendall_fails}
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

