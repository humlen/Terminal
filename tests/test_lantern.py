"""
Test lantern function
"""
import sys
sys.path.append("..")

from src.lantern import illuminate

ticker = 'MSFT'
df_is, df_bs, df_cf,df_kr, df_fund = illuminate(ticker)
print(df_cf.info())
print(df_cf['Cash Flow From Operating Activities -'])
# Test Income Statement
def test_lantern_IS_basedata():
    assert 'Revenue' in df_is

def test_lantern_IS_calcdata():
    assert 'Revenue TTM - QoQ' in df_is

def test_lantern_IS_values():
    assert max(df_is['EBITDA -']) > min(df_is['EBITDA -'])


# Test Balance Sheet
def test_lantern_BS_basedata():
    assert 'Cash On Hand -' in df_bs

def test_lantern_BS_calcdata():
    assert 'Share Holder Equity - YoY' in df_bs

def test_lantern_BS_values():
    assert max(df_bs['Total Current Assets -']) > \
    min(df_bs['Total Current Assets -'])


# Test Cash Flow Statement
def test_lantern_CF_basedata():
   assert 'Free Cash Flow' in df_cf 

def test_lantern_CF_calcdata():
    assert 'Capital Expenditure - QoQ'in df_cf

def test_lantern_CF_values():
    assert df_cf['Cash Flow From Operating Activities TTM'].max() > \
    df_cf['Cash Flow From Operating Activities TTM'].min()

# Test Key Ratios
def test_lantern_KR_basedata():
    assert 'Gross Margin' in df_kr

def test_lantern_KR_calcdata():
    assert 'Operating Margin - 5Y CAGR' in df_kr

def test_lantern_KR_values():
    assert max(df_kr['Operating Margin -'] > min(df_kr['Operating Margin -']))


# Test Fundamental Data


# Test Price Data
