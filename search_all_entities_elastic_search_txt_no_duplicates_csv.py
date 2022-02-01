# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 23:48:16 2021

@author: weixi
"""

#before running this, open elastic search http://localhost:9200/ and kibana localhost:5601/status

#output file: sentences_output.csv (sentences containing the entities)

#input file: all_entities.csv (entities) 'D:\DARPAproject\SBSpapers\training_data_processing\all_entities_version2_remove_duplicates.csv'

from elasticsearch import Elasticsearch
import csv
import pandas as pd
import numpy as np


def ElasticSearch(entityName):
    es = Elasticsearch(hosts="localhost:9200/", http_auth=())
    #print(es.info())
    
    #print("===================================================")
    
   
    query_json ={
      "query": {"match_phrase": {"sentence": entityName}}
    }
    
    
    query = es.search(index='sbsall',body=query_json, scroll='5m',size=100)  #scroll='1m' 代表 1min 后会释放
    #print(query)


    results = query['hits']['hits'] # es查询出的结果第一页
    total = query['hits']['total']  # es查询出的结果总量
    number_of_results = total['value']
    scroll_id = query['_scroll_id'] # 游标用于输出es查询出的所有结果
    
    
    for i in range(0, int(number_of_results/100)+1):
        # scroll参数必须指定否则会报错
        query_scroll = es.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
        
        results += query_scroll
    es.clear_scroll(scroll_id=scroll_id)    #clear scroll_id for every entity name, after it's searched
    
    return results
    
    
#=====================================load entity names from csv fils ==============================================================
file = open(r'D:\DARPAproject\SBSpapers\training_data_processing\all_entities_version2_remove_duplicates.csv') 
lines = file.readlines() 
names = []
field = []
for line in lines:
    line = line.strip()
    entity = line.split(',')[0]
    research_field = line.split(',')[1]
    #print(entity)  
    names.append(entity)
    field.append(research_field)
file.close()
#==================================================================================================================================



with open(r'D:\DARPAproject\SBSpapers\sentences_output_version2_no_duplicates.csv','w',newline='',encoding='utf-8') as flow:
    csv_writer = csv.writer(flow, delimiter=",")
    header=['id','sentence', 'sentencenumber', 'papernumber', 'entity', 'research_field']
    csv_writer.writerow(header)
    
    for i in range(len(names)):
        print("entity", i, "===================================================")
        entityName = names[i]
        results= ElasticSearch(entityName)
        entity = entityName
        fieldname = field[i]
        
    
        for res in results:
            # print(res)
            #csv_writer.writerow([res['_id']+','+res['_source']['sentence']+','+str(res['_source']['sentencenumber'])+','+str(res['_source']['papernumber'])])
            a= res['_id']
            b =res['_source']['sentence']
            c =str(res['_source']['sentencenumber'])
            d =str(res['_source']['papernumber'])
            #csv_writer.writerows([[a], [b], [c], [d]])  #
            csv_writer.writerows([[a, b, c, d, entity,fieldname]])  # one more [] : otherwise sepaerated each letter

print('done!')



#===============================================================
#query: match_ phrase:  match the whole phrase
#       match : match any word in this phrase
#
#es.clear_scroll(scroll_id=scroll_id):
# is used for solving this error:
#TransportError(500, 'search_phase_execution_exception', 'Trying to create too many scroll contexts. Must be less than or equal to: [500]. This limit can be set by changing the [search.max_open_scroll_context] setting.')
#================================================================