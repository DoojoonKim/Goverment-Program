# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 17:12:21 2018

@author: ChiHoon
"""
import pandas as pd
import numpy as np

def min_max(arg):
    number_types=[np.int,np.int0,np.int16,np.int32,np.int64,np.int8,
                  np.float,np.float16,np.float32,np.float64]
    for element in number_types:
        if arg.dtype == element:    
            return [arg.min(),arg.max()]
            




def struct(df):
    if isinstance(df, pd.DataFrame):
        df.info()
        print()               
        for element in df.columns:
            result = df[element]
            # magnitude = result.unique().size
            uni = result.unique()[:10]                
            print(element, ":", len(result.unique()), min_max(result), uni)


            


            
            
            

            
            
            
