# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 00:50:09 2021

@author: weixin
"""


from flair.data import Sentence
from flair.training_utils import EvaluationMetric
from flair.data import Corpus
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, TransformerWordEmbeddings
from typing import List
from flair.models import SequenceTagger
import json



# load the model you trained
model = SequenceTagger.load('resources/taggers/example-ner/final-model.pt')



#with open(r"/data/xwei/sbs_flair/sbs_sentences.json", 'r') as f:
with open(your_file_path, 'r') as f:  #use your path for input 'file'
    
    data = [json.loads(line) for line in f]
    data_dict = data[0]
    
    theory_dic = dict()
    for key in data_dict:   #  data_dict[key] is a list of sentences (the claimzone), key is the name of the claimzone
        #print(key+':'+data[key])
        print(key)
        #print(data_dict[key])
        print('=================================================================')
        
        TH = []
        for claim_sentence in data_dict[key]:
            #print(claim_sentence)
            #print('===')
            
            # create example sentence
            sentence = Sentence(claim_sentence)
            
            # predict tags and print
            model.predict(sentence)
            
            output = sentence.to_tagged_string()
            
            
            for string1 in sentence.get_spans('ner'):
                print(string1)
                string1 = str(string1)  # span object has no attribute split
                strint1_split = string1.split('   ')

                label1 = strint1_split[1].split(': ')  #['[− Labels', 'ASPECT (0.9998)]']
                label = label1[1].split(' (')[0]     #ASPECT
                
                entity = strint1_split[0].split(': ')[1]   #"front perspective view"
                entity = entity.split('"')    #['', 'front perspective view', '']
                entity = entity[1]          #front perspective view
                
                if label == "TH":
                    TH.append(entity)
                else:
                    TH = TH        
                
            
            #print("TH:", TH)
            
            
         
        theory_dic[key]=TH
        print("ttttTH:", TH) 
        #print(theory_dic)
    

with open(r"/data/xwei/sbs_flair/entity_number.json", "w") as f:
    json.dump(theory_dic,f)  
