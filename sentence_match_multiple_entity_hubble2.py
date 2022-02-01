# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 16:32:09 2021

@author: weixi
"""

# D:\DARPAproject\dictionary\all_entities_version2.csv

import re
import pandas as pd
import csv

#create a file to contain all outputs that the sentence can't match any entity (entity = [])
outfile = open('/data/xwei/sbspapers/entity_in_sentence_multiple2.csv','w', encoding="utf8", newline='')
writer1 = csv.writer(outfile)
header1=['sentence', 'entity']
writer1.writerow(header1)


#input all sentences 
file = open('/data/xwei/sbspapers/sentences_output_version2_remove_both_duplicates.tsv','r', encoding="utf8") #why encoding="utf8"? 'charmap' codec can't decode byte 0x90 in position 597: character maps to <undefined>
lines = file.readlines()
lines = lines[1:] # all except the first line: [1:]


#input all entities
file2 = open('/data/xwei/sbspapers/all_entities_version2_remove_duplicates2.csv','r')  #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3708: invalid continuation byte
lines2 = file2.readlines()
#lines2 = lines2[0:5]  # the first line is also entity name, so start from 0
#print(lines2)
entitys =[]
for line2 in lines2:
    line2 = line2.strip()
    entity = line2.split(',')[0]
    entity = re.sub(r'-+', ' ', entity)   #substitute - in the entity by space
    entity = re.sub(r"'", ' ', entity)    #substitute ' in the entity by space
    entity = re.sub(r"\?", ' ', entity)   #substitute ? in the entity by space
    entitys.append(entity)

n=0 #index for sentence
m=0 #number of cases a sentence having multiple entities in it
k=0 #number of cases a sentence matching 0 entities
all_matches=[]
for line in lines:
    n+=1
    print("n:",n)
    line = line.strip()
    sentence = line.split('\t')[1]
    sentence = re.sub(r'/+', ' ', sentence)  #substitute / in the sentence by space
    sentence = re.sub(r'-+', ' ', sentence)  #substitute - in the sentence by space
    sentence = re.sub(r"'", ' ', sentence)    #substitute ' in the sentence by space
    sentence = re.sub(r'"', ' ', sentence)    #substitute " in the sentence by space
    sentence = re.sub(r'\(', ' ', sentence)  #substitute ( in the sentence by space
    sentence = re.sub(r'\)', ' ', sentence)  #substitute ) in the sentence by space
    sentence = re.sub(r'\+', ' ', sentence)  #substitute + in the sentence by space
    
    match_outputs=[]
    for entity in entitys:
        match_output = re.search(entity, sentence, flags=re.I)   #flags=re.IGNORECASE is the same
        #print(match_output)
        if match_output != None:   #if type(match_output) == NoneType: can't work                Use None not 'None', not a string
            if not match_output.group() in match_outputs:
                match_outputs.append(match_output.group())
    #print(len(match_outputs))         # match_outputs is a list
    if len(match_outputs)>1:
        m+=1
    elif len(match_outputs)<1:
        k+=1
        writer1.writerow([sentence, match_outputs])
    
    all_matches.append(match_outputs)

print("m:", m)   
print("k:", k)     
outfile.close()


df = pd.DataFrame(all_matches)
df.to_csv('entity_in_sentence_multiple3.tsv', sep='\t', index=False, header=False)
#this file contains all sentences and corresponding entities, some of the entities may be [] (very few)