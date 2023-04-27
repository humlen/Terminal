"""
Math needed for Lantern project  
"""

import pandas as pd
import numpy as np


# Calculate QoQ and YoY metrics for Quarterly dataframe
def calculate_metric_q(dataframe, metric, modifier):
    """ Calculates standard metrics for quarterly data""" 

    dataframe[f"{metric} -"] = (
        pd.to_numeric(dataframe[f"{metric}"], errors = "coerce")
        .fillna(0)
    )

    # Check if the number should be multiplied by 1M or not
    if modifier == 1:
        dataframe[f"{metric} -"] = dataframe[f"{metric} -"].mul(1000000)
    elif modifier == 0:
        pass

    # Calculate change Quarter over Quarter
    dataframe[f"{metric} - QoQ"] = (
            dataframe[f"{metric} -"]
            .pct_change(1)
            .fillna(0)
            .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    # Calculate change Year over Year
    dataframe[f"{metric} - YoY"] = (
        dataframe[f"{metric} -"]
        .pct_change(4)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    return dataframe



# Calculate QoQ, YoY and 5Y metrics for Trailing Twelve Month data
def calculate_metric_ttm(dataframe, metric, modifier):
    """ Calculates standard metrics for trailing twelve month data"""

    dataframe[f"{metric} -"] = (
        pd.to_numeric(dataframe[f"{metric}"], errors = "coerce")
        .fillna(0)
    )

    # Check if the number should be multiplied by 1M or not
    if modifier == 1:
        dataframe[f"{metric} -"] = dataframe[f"{metric} -"].mul(1000000)
    elif modifier == 0:
        pass

    # Trailing Twelve Month Data
    dataframe[f"{metric} TTM"] = dataframe[f"{metric} -"].rolling(4).sum()

    # Calculate TTM Quarter over Quarter
    dataframe[f"{metric} TTM - QoQ"] = (
        dataframe[f"{metric} TTM"]
        .pct_change(1)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    # Calculate TTM Year over Year
    dataframe[f"{metric} TTM - YoY"] = (
        dataframe[f"{metric} TTM"]
        .pct_change(4)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    # Calculate TTM 5 Year Annual Growth Rate
    dataframe[f"{metric} TTM - 5Y CAGR"] = (
        pow(dataframe[f"{metric} TTM"]
        .pct_change(20)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x) + 1, 0.2) - 1
    )

    return dataframe



def calculate_metric_static(dataframe, metric, modifier):
    """ Calculates standard metrics for static data """

    dataframe[f"{metric} -"] = (
        pd.to_numeric(dataframe[f"{metric}"], errors = "coerce")
        .fillna(0)
    )

    if modifier == 1:
        dataframe[f"{metric} -"] = dataframe[f"{metric} -"].mul(1000000)

    elif modifier == 2:
        dataframe[f"{metric} -"] = dataframe[f"{metric} -"].div(100)

    # Calculate Quarter over Quarter
    dataframe[f"{metric} - QoQ"] = (
        dataframe[f"{metric} -"]
        .pct_change(1)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    # calculate Year over Year
    dataframe[f"{metric} - YoY"] = (
        dataframe[f"{metric} -"]
        .pct_change(4)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x)
    )

    # Calculate 5 Year Annual Growth Rate
    dataframe[f"{metric} - 5Y CAGR"] = (
        pow(dataframe[f"{metric} -"]
        .pct_change(20)
        .fillna(0)
        .apply(lambda x: 0 if not np.isfinite(x) else x) + 1, 0.2) - 1
    )

    return dataframe


# Calculate Quantiles
def calculate_quantiles(dataframe, numerator, denominator, product_name):
    """Calculate the upper and lower quantiles of a relative metric"""
    dataframe[f"{product_name}"] = dataframe[f"{numerator}"]/dataframe[f"{denominator}"] * 100
    dataframe[f"{product_name} Lower Quintile"] = (
        dataframe[f"{product_name}"].rolling(1460).quantile(.15, interpolation = 'midpoint'))
    dataframe[f"{product_name} Upper Quintile"] = (
        dataframe[f"{product_name}"].rolling(1460).quantile(.85, interpolation = 'midpoint'))
