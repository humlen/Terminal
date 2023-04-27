
'''
Testing functions from the Pearson.py module
'''

import sys
sys.path.append("..") # needed to find relative path
from src.pearson import pearson_ranker #type: ignore

def test_pearson_revenue_msft():
    ticker = ['MSFT']
    metric = 'revenue'
    df_output = pearson_ranker(ticker, metric)[0]
    x = df_output[0]['pearson r'].iloc[0]

    assert (-1 <= x <= 1)

def test_pearson_revenue_msft_errors():
    ticker = ['This is a test']
    metric = 'revenue'
    error = pearson_ranker(ticker, metric)[1]
    
    assert error == 1 

# TODO: Add a numeric or size checker on this function
def test_pearson_revenue_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'revenue'
    df_output = pearson_ranker(ticker, metric)[0]
    
    # assert is_numeric_dtype(df_output['pearson r']) == True


def test_pearson_revenue_quarters():
    ticker = ['MSFT']
    metric = 'revenue'
    df_output = pearson_ranker(ticker,metric)[0]
    x = df_output[0]['pearson quarters'].iloc[0]

    assert x > 0


# Net Income Tests
def test_pearson_netincome_msft():
    ticker = ['MSFT']
    metric = 'netincome'
    df_output = pearson_ranker(ticker, metric)[0]
    x = df_output[0]['pearson r'].iloc[0]

    assert (-1 <= x <= 1)

def test_pearson_netincome_msft_errors():
    ticker = ['This is a test']
    metric = 'netincome'
    error = pearson_ranker(ticker, metric)[1]
    
    assert error == 1 

# TODO: Add a numeric or size checker on this function
def test_pearson_netincome_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'netincome'
    df_output = pearson_ranker(ticker, metric)[0]

    # missing assertion

def test_pearson_netincome_quarters():
    ticker = ['MSFT']
    metric = 'netincome'
    df_output = pearson_ranker(ticker,metric)[0]
    x = df_output[0]['pearson quarters'].iloc[0]

    assert x > 0 


# EPS Tests
def test_pearson_eps_msft():
    ticker = ['MSFT']
    metric = 'eps'
    df_output = pearson_ranker(ticker, metric)[0]
    x = df_output[0]['pearson r'].iloc[0]

    assert (-1 <= x <= 1)

def test_pearson_eps_msft_errors():
    ticker = ['This is a test']
    metric = 'eps'
    error = pearson_ranker(ticker, metric)[1]
    
    assert error == 1 

# TODO: Add a numeric or size checker on this function
def test_pearson_eps_multiple():
    ticker = ['MSFT','GOOG','AAPL','AMZN']
    metric = 'eps'
    df_output = pearson_ranker(ticker, metric)[0]

    # missing assertion
def test_pearson_eps_quarters():
    ticker = ['MSFT']
    metric = 'eps'
    df_output = pearson_ranker(ticker,metric)[0]
    x = df_output[0]['pearson quarters'].iloc[0]

    assert x > 0


# Net Income Tests
