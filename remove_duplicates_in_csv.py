# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 14:06:27 2021

@author: weixi
"""

import pandas as pd
import csv

l = list()
with open('all_entities_version2.csv','r') as read:
    reader = csv.reader(read)
    for i in reader:
        l.append(i)
df = pd.DataFrame(l)  #l is a list, from list to dataframe
df[0] = df[0].str.lower()  #make all the elements in the first column lower case
df.drop_duplicates(subset=0,inplace=True)   
df.reset_index(drop=True, inplace=True)  #reset index
#df.to_csv('all_entities_version2_remove_duplicates.csv')  # create a new .csv file, output the deleted file
df.to_csv('all_entities_version2_remove_duplicates2.csv', index=False, header=False) # no index in the first column, no column name in the first row




#===================================================================================================
#df.drop_duplicates(subset='column name',keep='first', inplace=True)   
# subset='column name', if no column name, the first column is 0, only consider first column
#keep : 'first'，'last'，False
#inplace=False: does not replace it. We need to use "inplace=True"
#reset_index，默认(drop = False)，当我们指定(drop = True)时，则不会保留原来的index，会直接使用重置后的索引。
# we need to use "drop=True, inplace=True" both 
#===================================================================================================
#df.drop_duplicates(subset=0,inplace=True)  
#代码中subset对应的值是列名，表示只考虑这两列，将这两列对应值相同的行进行去重。默认值为subset=None表示考虑所有列。



#===================================================================================================
#Create a csv file:
#df.to_csv('filename.csv', header=False, index=False)
#Create a txt? file:
#df.to_csv('filename.tsv', sep='\t', header=False, index=False) 
#===================================================================================================
