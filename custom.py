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
            uni = result.unique()
            print(element, ":", '범위:',min_max(result),'유일값수:',len(uni), uni[:10])
            
class matplot_hangul:
    def __init__(self):
        import platform
        import matplotlib.pyplot as plt
        from matplotlib import font_manager, rc
        # 한글처리
        plt.rcParams['axes.unicode_minus'] = False
        if platform.system() == 'Darwin':    # 맥
            rc( 'font', family='AppleGothic' )
        elif platform.system() == 'Windows': # 윈도우
            # 폰트 차후 확인
            fontPath = 'c:/Windows/Fonts/malgun.ttf'
            fontName = font_manager.FontProperties( fname=fontPath ).get_name()
            rc( 'font', family=fontName )
        else:
            print('알수없는 시스템. 미적용')


            


            
            
            

            
            
            
