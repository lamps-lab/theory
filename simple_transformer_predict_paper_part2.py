# -*- coding: utf-8 -*-
"""
Created on Mon May 10 00:52:39 2021

@author: weixi
"""

import ast
from xml.dom.minidom import parse

import json
import os
import logging
import pandas as pd
from simpletransformers.ner import NERModel, NERArgs
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"



file = open('/data/xwei/sbspapers/sentences.txt','r', encoding="utf8") #why encoding="utf8"? 'charmap' codec can't decode byte 0x90 in position 597: character maps to <undefined>
all_sentences = file.readline()  
list_all_sentences = ast.literal_eval(all_sentences) #convert integer to list
                

#============================Part 2: Use model to find entities in sentences===========================================                
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)


model_args = NERArgs()

model_args.labels_list = ["B-TH", "I-TH", "O"]

#use the trained model, specify the path to the model
model = NERModel(
    "roberta", '/data/xwei/sbspapers/outputs/', args=model_args
)



predictions, raw_outputs = model.predict(all_sentences)  #a list of strings


#print(predictions)      #output is a list of lists 


#This is to extract the entities from the prediction outputs
entity_all_sentences=[]
for i in range(len(predictions)):
    entity=[]
    for j in range(len(predictions[i])):
        p = list(predictions[i][j].items())  #p: [('For', 'O')]
      
        if p[0][1] !='O':
            entity_token =p[0][0]
        else:
            entity_token = ' '
        entity.append(entity_token)
          
    entity_all_sentences.append(entity)

#print(entity_all_sentences)



df = pd.DataFrame(entity_all_sentences)
df.to_csv('extracted_entity_in_papers.tsv', sep='\t', index=False, header=False)





#outfile = open('extracted_entity_in_papers.txt','w', encoding="utf8");

#outfile.write(str(entity_all_sentences));

#outfile.close();