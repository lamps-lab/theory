# -*- coding: utf-8 -*-
"""
Created on Mon May 10 00:52:39 2021

@author: weixi
"""

from xml.dom.minidom import parse
import stanza
import json
import os
import logging
import pandas as pd
from simpletransformers.ner import NERModel, NERArgs
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


#============================Part I: segmentation of papers into sentences===========================================
def allChildren(node):
    content = ''
    nodelist = node.childNodes
    for node in nodelist:
        if node.nodeType != node.TEXT_NODE:
            content = content + allChildren(node)
        else:
            nodedata = node.data
            content = content + nodedata
    return content

def tokenize(text):
    textnlp = nlp(text)
    return [sentence.text for sentence in textnlp.sentences]



nlp = stanza.Pipeline(lang='en', processors='tokenize,ner', use_gpu=False)


file_dir = r'/data/xwei/processedSBSpapers1to1000' # need r, otherwise no output
n = 0
m = 0
all_sentences = []
for dirpath, dirnames, filenames in os.walk(file_dir):  
    for file in filenames :  
        if os.path.splitext(file)[1] == '.xml':  #file name is Abaluck_AmEcoRev_2016_Akjj.tei.xml, but index for xml is still 1
            pfname = file_dir +"/" + file  # path
            papername = file           # only the file, not path
            
            print(pfname)
            
            m +=1
            print("m:", m)
            
            try:
                doc = parse(pfname)
                                             
                divs = doc.getElementsByTagName('div')
                
                
                id = 0
                for div in divs:
                    paragraphs = div.getElementsByTagName('p')
                    for p in paragraphs:
                        pdata = allChildren(p)
                        #print(pdata)
                        #print("\n")
                        sentences = tokenize(pdata)
                        for sentence in sentences:
                            all_sentences.append(sentence)
                            
            except Exception as e:
                print('')                
                

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



predictions, raw_outputs = model.predict(all_sentences)


print(predictions)      #output is a list of lists 


#This is to extract the entities from the prediction outputs
entity=[]
entity_all_sentences=[]
for i in range(len(predictions)):
   for j in range(len(predictions[i])):
      p = list(predictions[i][j].items())  #p: [('For', 'O')]
      
      if p[0][1] !='O':
          entity_token =p[0][0]
          entity.append(entity_token)
          
    entity_all_sentences.append(entity)

print(entity_all_sentences)
