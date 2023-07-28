"""
@author: eirik
@date: 2023-01-13

A tool to collect basic information about a company, and export it in a format
compatible with a premade PowerBI-Report
"""

# Import Packages
from urllib.request import Request, urlopen
import warnings
import time
from datetime import datetime
from .scraper_mt import scrape_mt

import pandas as pd
import yfinance as yf
import numpy as np
from bs4 import BeautifulSoup
from .calculations_metrics import calculate_metric_q, calculate_metric_static,\
    calculate_metric_ttm, calculate_quantiles
from .spotlight_output import lantern_writer

# Caveats and config
warnings.filterwarnings("ignore")

# Config
VERSION_NAME = "Spotlight"
VERSION_NUMBER = "1.0"


def illuminate(ticker):
    """Discovery tool to perform an automated due dilligence on a given equity. 
    With a single input (the ticker of the equity), we are able to scrape data 
    ranging from simple revenue metrics to specific reported costs, relative 
    valuations and share issuance / buybacks. The output is presented in the 
    Lantern PowerBI report.
    """

    # Links & Shorthands
    # link_db = "C:/Users/eirik/Codebase/Database"
    # link_pb = "C:/Users/eirik/Codebase/Reports/PowerBI Resources"
    link_mt = "https://www.macrotrends.net/stocks/charts"
    
    link_db = "../Database"
    link_pb = "../Reports/PowerBI Resources"

        
    # Definitions
    master_tickers = pd.read_csv(f"{link_db}/master__tickers.csv")
    meta_stock = master_tickers.loc[master_tickers['ticker'] == ticker]
    comp = meta_stock["comp_name"].values
    comp = str(comp).translate(str.maketrans("", "", "[]'\""))
    comp_b = meta_stock["comp_name_2"].values
    comp_b = str(comp_b).translate(str.maketrans("", "", "[]'\""))

    # URLs
    link_is = f"{link_mt}/{ticker}/{comp}/income-statement?freq=Q"
    link_bs = f"{link_mt}/{ticker}/{comp}/balance-sheet?freq=Q"
    link_cf = f"{link_mt}/{ticker}/{comp}/cash-flow-statement?freq=Q"
    link_kr = f"{link_mt}/{ticker}/{comp}/financial-ratios?freq=Q"
    link_fv = f"https://finviz.com/quote.ashx?t={ticker}&p=d"

    # Variables
    start_date = "2015-01-01"

    # Lists & Counters
    start_time = time.time()
    ticker = ticker.upper()

    # Launch
    print ('Getting data for ' + comp_b + '...\n')

    # Scrape MT
    df_is = scrape_mt(link_is)
    
    list_is_full_q = [
        "Revenue", "Net Income", "EBITDA", 
        "Operating Expenses","SG&A Expenses"]
    list_is_full_ttm = [
        "Revenue", "Net Income", "EBITDA", 
        "Operating Expenses"]
    list_is_static = ["Shares Outstanding"]
    list_is_full_nomult = ["EPS - Earnings Per Share"]

    # Standard Metrics
    for list_items in list_is_full_q:
        calculate_metric_q(df_is,list_items,1)

    for list_items in list_is_full_ttm:
        calculate_metric_ttm(df_is,list_items,1)

    for list_items in list_is_full_nomult:
        calculate_metric_q(df_is,list_items,0)
        calculate_metric_ttm(df_is,list_items,0)

    for list_items in list_is_static:
        calculate_metric_static(df_is,list_items,1)

    # SG&A Metrics
    df_is["SG&A TTM"] = df_is["SG&A Expenses -"].rolling(4).sum()
    df_is["SG&A Percentage of Revenue"] = df_is["SG&A TTM"]/df_is["Revenue TTM"]
    df_is["SG&A Percentage of Revenue - QoQ"] = (
        df_is["SG&A Percentage of Revenue"]
        .pct_change(1)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )
    df_is["SG&A Percentage of Revenue - YoY"] = (
        df_is["SG&A Percentage of Revenue"]
        .pct_change(4)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )
    df_is["SG&A Percentage of Revenue - 5Y CAGR"] = (
        pow(df_is['SG&A Percentage of Revenue']
        .pct_change(20)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x) + 1, 0.2) - 1
    )

    # Revenue / Net Income
    df_is["Revenue / Net Income"] = df_is["Revenue TTM"]/df_is["Net Income TTM"]
    df_is["Revenue / Net Income Lower Quintile"] = df_is["Revenue / Net Income"].quantile(.2)
    df_is["Revenue / Net Income Upper Quintile"] = df_is["Revenue / Net Income"].quantile(.8)

    # Finish Income Statement
    print('Income Statement finished in :'+str(round((time.time() - start_time),3))+' Seconds')


    # Balance Sheet
    df_bs = scrape_mt(link_bs)

    list_bs_static = ["Cash On Hand","Total Current Assets",
    "Total Current Liabilities","Total Liabilities",
    "Share Holder Equity","Long Term Debt"]

    for list_items in list_bs_static:
        calculate_metric_static(df_bs,list_items,1)

    # Finish Balance Sheet
    print('Balance Sheet finished in :'+str(round((time.time() - start_time),3))+' Seconds')


    # Cash Flow Statement
    df_cf = scrape_mt(link_cf)    

    list_cf_full = ["Cash Flow From Operating Activities",
    "Cash Flow From Investing Activities","Cash Flow From Financial Activities",
    "Stock-Based Compensation","Net Common Equity Issued/Repurchased", 
    "Common Stock Dividends Paid"]

    for list_items in list_cf_full:
        calculate_metric_q(df_cf,list_items,1)
        calculate_metric_ttm(df_cf,list_items,1)

    # Capital Expenditure
    
    try:
        df_cf["Capital Expenditure"] = (
            df_cf["Total Depreciation And Amortization - Cash Flow"]
            .fillna(0).astype("float64") + df_cf["Net Change In Property, Plant, And Equipment"]
            .fillna(0).astype("float64")
        )
        df_cf["Capital Expenditure - QoQ"] = (
            df_cf["Capital Expenditure"]
            .pct_change(1)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Capital Expenditure - YoY"] = (
            df_cf["Capital Expenditure"]
            .pct_change(4)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Capital Expenditure TTM"] = df_cf["Capital Expenditure"].rolling(4).sum()
        df_cf["Capital Expenditure TTM - QoQ"] = (
            df_cf["Capital Expenditure TTM"]
            .pct_change(1)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Capital Expenditure TTM - YoY"] = (
            df_cf["Capital Expenditure TTM"]
            .pct_change(4)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Capital Expenditure TTM - 5Y CAGR"] = (
            pow(df_cf['Capital Expenditure TTM']
                .pct_change(20)
                .fillna(0)
                .apply(lambda x: 0 if not np.isfinite(x) else x) + 1, 0.2) - 1
        )
    
    except:
        df_cf["Capital Expenditure"] = 0
        df_cf["Capital Expenditure - QoQ"] = 0
        df_cf["Capital Expenditure - YoY"] = 0
        df_cf["Capital Expenditure TTM"] = 0
        df_cf["Capital Expenditure TTM - QoQ"] = 0
        df_cf["Capital Expenditure TTM - YoY"] = 0
        df_cf["Capital Expenditure TTM - 5Y CAGR"] = 0


        # Free Cash Flow
    try: 
        df_cf["Free Cash Flow"] = (
            df_cf["Cash Flow From Operating Activities -"] - df_cf["Capital Expenditure"]
        )
        df_cf["Free Cash Flow - QoQ"] = (
            df_cf["Free Cash Flow"]
            .pct_change(1)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Free Cash Flow - YoY"] = (
            df_cf["Free Cash Flow"]
            .pct_change(4)
            .fillna(0).apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Free Cash Flow TTM"] = df_cf["Free Cash Flow"].rolling(4).sum()
        df_cf["Free Cash Flow TTM - QoQ"] = (
            df_cf["Free Cash Flow TTM"]
            .pct_change(1)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Free Cash Flow TTM - YoY"] = (
            df_cf["Free Cash Flow TTM"]
            .pct_change(4)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
        )
        df_cf["Free Cash Flow TTM - 5Y CAGR"] = (
            pow(df_cf['Free Cash Flow TTM']
                .pct_change(20)
                .fillna(0)
                .apply(lambda x: 0 if not np.isfinite(x) else x) + 1, 0.2) - 1
        )

    except:
        df_cf["Free Cash Flow"] = 0
        df_cf["Free Cash Flow - QoQ"] = 0
        df_cf["Free Cash Flow - YoY"] = 0
        df_cf["Free Cash Flow TTM"] = 0
        df_cf["Free Cash Flow TTM - QoQ"] = 0
        df_cf["Free Cash Flow TTM - YoY"] = 0
        df_cf["Free Cash Flow TTM - 5Y CAGR"] = 0


    # Finish Cash Flow Statement
    print('Cash Flow Statement finished in :'+str(round((time.time() - start_time),3))+' Seconds')

    # Key Ratios
    df_kr = scrape_mt(link_kr)

    list_kr_static_percentage = ["Gross Margin","Operating Margin","ROI - Return On Investment"]

    for list_items in list_kr_static_percentage:
        calculate_metric_static(df_kr,list_items,2)

    # Finish Key Ratios
    print('Key Ratios finished in :'+str(round((time.time() - start_time),3))+' Seconds')


    # Price Data
    stock = yf.Ticker(ticker)
    stock_all = stock.history(period="max")
    df_histprice = stock_all[["Close"]]

    # SMA
    df_histprice["50d SMA"] = df_histprice["Close"].rolling(window = 50).mean()
    df_histprice["250d SMA"] = df_histprice["Close"].rolling(window = 250).mean()
    df_histprice["Date"] = df_histprice.index
    df_histprice = df_histprice[df_histprice.index>=start_date]
    df_histprice_cols = df_histprice.columns.tolist()
    df_histprice_cols = df_histprice_cols[-1:] + df_histprice_cols[:-1]
    df_histprice = df_histprice[df_histprice_cols]
    df_dates = pd.DataFrame({'Date':pd.date_range(start=start_date, end=datetime.today())})
    df_histprice = df_histprice.reset_index(drop=True)
    df_histprice['Date'] = df_histprice['Date'].dt.tz_localize(None)
    df_price_raw = pd.merge(df_dates, df_histprice, how = 'left', left_on='Date', right_on = 'Date')
    df_price_raw = df_price_raw.ffill(axis=0)


    # Other Metrics
        # Revenue / MCap
    df_shares = df_is[["Date","Shares Outstanding -","Revenue TTM"]]
    df_shares = df_shares.astype({"Date": 'datetime64[ns]'})
    df_price = df_price_raw.merge(df_shares, how="left", left_on = "Date", right_on = "Date")
    df_price = df_price.ffill(axis=0)
    df_price["Market Capitalization"] = df_price["Close"]*df_price["Shares Outstanding -"]
    df_price = df_price.dropna()

    calculate_quantiles(
        df_price, "Revenue TTM", "Market Capitalization", "Revenue / Market Capitalization")

        # EBITDA / MCap With Quantiles
    df_ebidta = df_is[["Date","EBITDA TTM"]]
    df_ebidta = df_ebidta.astype({"Date": 'datetime64[ns]'})
    df_price = df_price.merge(df_ebidta, how = "left", left_on = "Date", right_on = "Date")
    df_price = df_price.ffill(axis=0)

    calculate_quantiles(
        df_price, "EBITDA TTM", "Market Capitalization", "EBITDA / Market Capitalization")

        # Free Cash Flow / MCap With Quantiles
    df_fcf = df_cf[["Date","Free Cash Flow TTM"]]
    df_fcf = df_fcf.astype({"Date": 'datetime64[ns]'})
    df_price = df_price.merge(df_fcf, how = "left", left_on = "Date", right_on = "Date")
    df_price = df_price.ffill(axis = 0)
    df_price["FCF / Market Capitalization"] = (
        df_price["Free Cash Flow TTM"] / df_price["Market Capitalization"] * 100
    )
    df_price["FCF / Market Capitalization Lower Quintile"] = (
        df_price["FCF / Market Capitalization"]
        .rolling(1460)
        .quantile(.15, interpolation = 'lower')
    )
    df_price["FCF / Market Capitalization Upper Quintile"] = (
        df_price["FCF / Market Capitalization"]
        .rolling(1460)
        .quantile(.85, interpolation = 'lower')
    )

        # Boundary Validity
    df_boundarytest = df_price
    df_boundarytest["Daily Change"] = df_boundarytest["Close"].pct_change(1)
    df_boundarytest["Daily Change Norm"] = df_boundarytest["Daily Change"] + 1

        # Finish Price Data
    print('Price Data finished in :'+str(round((time.time() - start_time),3))+' Seconds')


    # Set up scraper
    req = Request(link_fv, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = BeautifulSoup(webpage, "html.parser")

    # Find fundamentals table
    fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]

    # Clean up fundamentals dataframe
    fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    colone = []
    collength = len(fundamentals)
    for k in np.arange(0, collength, 2):
        colone.append(fundamentals[f'{k}'])
    attrs = pd.concat(colone, ignore_index=True)

    coltwo = []
    collength = len(fundamentals)
    for k in np.arange(1, collength, 2):
        coltwo.append(fundamentals[f'{k}'])
    vals = pd.concat(coltwo, ignore_index=True)

    fundamentals = pd.DataFrame()
    fundamentals['Attributes'] = attrs
    fundamentals['Values'] = vals
    fundamentals = fundamentals.set_index('Attributes')

    # Fix missing values
    df_fundamentals = fundamentals.T
    df_fundamentals["ticker"] = ticker
    df_fundamentals["company"] = comp
    df_fundamentals["company_b"] = comp_b
    df_fundamentals["version_name"] = VERSION_NAME
    df_fundamentals["version_number"] = "version "+VERSION_NUMBER
    df_fundamentals.replace("-", 0, inplace=True)

    # Finish Fundamental Data
    print('Fundamental Data finished in :'+str(round((time.time() - start_time),3))+' Seconds')

    # Write to Excel
    lantern_writer(df_is, df_bs, df_cf, df_kr, df_fundamentals, df_price)
    print('Excel Export finished in :'+str(round((time.time() - start_time),3))+' Seconds')
    
    # Return datasets and end execution
    print("Execution time:  "+str(round((time.time() - start_time),3 ))+" seconds")
    return df_is, df_bs, df_cf, df_kr, df_fundamentals

