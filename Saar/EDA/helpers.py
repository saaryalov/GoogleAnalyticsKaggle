import pandas as pd
import numpy as np

def custom_mean(df):
    return df.mean(skipna=True)
def custom_sum(df):
    return df.sum(skipna=True)


def sort_by_rev(df,col,kind = "mean"):
    # Value counts sort 
    sort = df[col].value_counts(normalize=True).to_frame("Frequency")
    sort.index.name = col
    sort = sort.reset_index(col_fill = col)
    
    # Group by col and revenue
    gby = df.groupby(col)["totals.transactionRevenue"]
    if kind.lower() == "sum":
        gby = gby.agg(custom_sum).reset_index()
    else:
        gby = gby.agg(custom_mean).reset_index()
    
    result = sort.merge(gby,on=col)
    #sum_rev = sum(result["totals.transactionRevenue"]>thresh)
    return result


# Manual FE
def manual_ohe(col,level,name=None):
    # The goal of this function is to manually OHE features 
    assert isinstance(col,str)
    if isinstance(level,str):
        level = level.replace(" ","_")
        train[col+"__"+level] = train[col].map(lambda x: (x == level)*1)
        test[col+"__"+level] = test[col].map(lambda x: (x == level)*1)
    elif isinstance(level,list):
        train[col+"__"+name] = train[col].map(lambda x: (x in level)*1)
        test[col+"__"+name] = train[col].map(lambda x: (x in level)*1)
    else:
        print("ERROR WITH ", col, "!")

