'''
Testing functions from the spearman.py module
'''

import sys
sys.path.append("..") # needed to find relative path
from src.spearman import spearman_ranker #type: ignore

def test_spearman_revenue_msft():
    ticker = ['MSFT']
    metric = 'revenue'
    df_output = spearman_ranker(ticker, metric)[0]
    x = df_output[0]['spearman r'].iloc[0]

    assert (-1 <= x <= 1)

def test_spearman_revenue_msft_errors():
    ticker = ['This is a test']
    metric = 'revenue'
    error = spearman_ranker(ticker, metric)[1]
    
    assert error == 1 # Red

def test_spearman_revenue_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'revenue'
    df_output = spearman_ranker(ticker, metric)[0]
    
    # assert is_numeric_dtype(df_output['spearman r']) == True

    
def test_spearman_revenue_quarters():
    ticker = ['MSFT']
    metric = 'revenue'
    df_output = spearman_ranker(ticker,metric)[0]
    x = df_output[0]['spearman quarters'].iloc[0]

    assert x > 0


# Net Income Tests
def test_spearman_netincome_msft():
    ticker = ['MSFT']
    metric = 'netincome'
    df_output = spearman_ranker(ticker, metric)[0]
    x = df_output[0]['spearman r'].iloc[0]

    assert (-1 <= x <= 1)

def test_spearman_netincome_msft_errors():
    ticker = ['This is a test']
    metric = 'netincome'
    error = spearman_ranker(ticker, metric)[1]
    
    assert error == 1 # Red

def test_spearman_netincome_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'netincome'
    df_output = spearman_ranker(ticker, metric)[0]

    # missing assertion

def test_spearman_netincome_quarters():
    ticker = ['MSFT']
    metric = 'netincome'
    df_output = spearman_ranker(ticker,metric)[0]
    x = df_output[0]['spearman quarters'].iloc[0]

    assert x > 0 


# EPS Tests
def test_spearman_eps_msft():
    ticker = ['MSFT']
    metric = 'eps'
    df_output = spearman_ranker(ticker, metric)[0]
    x = df_output[0]['spearman r'].iloc[0]

    assert (-1 <= x <= 1)

def test_spearman_eps_msft_errors():
    ticker = ['This is a test']
    metric = 'eps'
    error = spearman_ranker(ticker, metric)[1]
    
    assert error == 1

def test_spearman_eps_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'eps'
    df_output = spearman_ranker(ticker, metric)[0]

    # missing assertion
def test_spearman_eps_quarters():
    ticker = ['MSFT']
    metric = 'eps'
    df_output = spearman_ranker(ticker,metric)[0]
    x = df_output[0]['spearman quarters'].iloc[0]

    assert x > 0

