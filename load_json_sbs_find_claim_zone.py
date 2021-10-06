# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:49:35 2021

@author: weixin
"""

import json

with open(r'C:/Users/weixi/Downloads/score_psu-claimevidence/score_psu-claimevidence/pipeline/claimevidence.jsonl', 'r') as f:
    #lines = json.load(f)
    data = [json.loads(line) for line in f]
    
    sentences = dict()
    for dict_line in data:
        paper_id = dict_line['paper_id'] 
        claims = dict_line['claims']
        
        claimidlist=[]
        claim_temp = 0
        
        paragraphid_temp = []
        for claim in claims:
            claimid= claim['claimid']
            paragraphid = claim['paragraphid']
            claim_index = paper_id + '_' + str(claimid)
            
            if claimid != claim_temp:
                claim_temp = claimid
                paragraphid_temp = []
                paragraphid_temp.append(paragraphid)
                paragraphtext = claim['paragraphtext']
                sentences[claim_index] = []
                sentences[claim_index].extend(paragraphtext)
                
            elif claimid == claim_temp:
                if paragraphid not in paragraphid_temp:
                    paragraphtext = claim['paragraphtext']
                    #sentences.append(paragraphtext)
                    paragraphid_temp.append(paragraphid)
                    sentences[claim_index].extend(paragraphtext)
            
            
                
with open(r"C:\Users\weixi\Dropbox\sbs\sbs_sentences.json", "w") as f:
    json.dump(sentences,f)            
            
            
            
                
            
           # paragraphid = claim['paragraphid']
           # label = claim['label']
           # claimidlist.append(claimid)
           