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

