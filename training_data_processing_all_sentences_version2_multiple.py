# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 15:58:10 2021

@author: weixi
"""

import nltk
import re
import os
import csv
#os.environ["CUDA_VISIBLE_DEVICES"] = "2"


#nltk.download('punkt')  #download this then you are able to use nltk. run this command once


#file = open(r'/data/xwei/traindata_darpa/sentences_output_version2.txt','r', encoding="utf8")

#output the bad ones (can't match entity in the sentence)
memo1 = open(r'D:\DARPAproject\SBSpapers\training_data_processing\memo_multi1.csv','w', encoding="utf8", newline='')
writer1 = csv.writer(memo1)
header1=['sentence', 'entity', 'index']
writer1.writerow(header1)

#output the tokens that can't be encoded
memo2 = open(r'D:\DARPAproject\SBSpapers\training_data_processing\memo_multi2.csv','w', encoding="utf8", newline='')
writer2 = csv.writer(memo2)
header2=['sentence', 'NA']
writer2.writerow(header2)

#output the bad ones with multiple entities
memo3 = open(r'D:\DARPAproject\SBSpapers\training_data_processing\memo_multi3.csv','w', encoding="utf8", newline='')
writer3 = csv.writer(memo3)
header3=['sentence', 'index', 'entities']
writer3.writerow(header3)


file = open(r'D:\DARPAproject\SBSpapers\training_data_processing\sentences_output_version2_remove_both_duplicates.tsv','r', encoding="utf8") 
#why encoding="utf8"? 'charmap' codec can't decode byte 0x90 in position 597: character maps to <undefined>
lines = file.readlines()
lines = lines[1:] # all except the first line: [1:]
#lines = lines[28251:28342]

file_entity = open(r'D:\DARPAproject\SBSpapers\training_data_processing\entity_in_sentence_multiple3.tsv','r', encoding="utf8") 
#file_entity = open(r'D:\DARPAproject\SBSpapers\training_data_processing\entity_in_sentence_multiple_30000samples.tsv','r', encoding="utf8") 
#why encoding="utf8"? 'charmap' codec can't decode byte 0x90 in position 597: character maps to <undefined>
lines_entity = file_entity.readlines()
lines_entity = lines_entity[0:] # all except the first line: [1:]
#lines_entity = lines_entity[28250:28341]

n=0
nn=0    #total bad number
bad = []
for lll in range(0, len(lines)):
    #the relation of n and lll:  n = lll + 1
    n+=1
    #print("n:",n)
    line = lines[lll]
    line = line.strip()
    
    sentence = line.split('\t')[1]
    sentence = re.sub(r'/+', ' ', sentence)  #substitute / in the sentence by space
    sentence = re.sub(r'-+', ' ', sentence)  #substitute - in the sentence by space
    sentence = re.sub(r"'", ' ', sentence)    #substitute ' in the sentence by space
    sentence = re.sub(r'"', ' ', sentence)    #substitute " in the sentence by space
    sentence = re.sub(r'\(', ' ', sentence)  #substitute ( in the sentence by space
    sentence = re.sub(r'\)', ' ', sentence)  #substitute ) in the sentence by space
    sentence = re.sub(r'\+', ' ', sentence)  #substitute + in the sentence by space
    #tokens = sentence.split()
    tokens = nltk.word_tokenize(sentence)
    
    entity_multi = lines_entity[lll]

    entity_multi = entity_multi.split('\t')  #this can not work in .csv file, because the second element is a sentence, this sentence may contain ","
    

    
    while '' in entity_multi:
        entity_multi.remove('')
    while '\n' in entity_multi:
        entity_multi.remove('\n')
    #remove empty string in the list  
    #['attribution theory', 'self-determination theory', 'determinatio', 'self-determination', '', '\n']

    if entity_multi == []:
        print(len(entity_multi))
        print("n:",n)
        bad.append(n)
        nn+=1

    #path = os.path.join('/data/xwei/traindata_darpa/','all_txt_files',str(n)+'.txt')
    path = os.path.join('D:\DARPAproject\\SBSpapers\\training_data_processing','all_txt_files',str(n)+'.txt')
    #outfile = open(str(n) + '.txt', 'w')
    outfile = open(path, 'w')

    
    if len(entity_multi)==1:
        #print("mark1********************")
        entity = entity_multi[0]
        entity = re.sub(r'-+', ' ', entity)   #substitute - in the entity by space
        entity = re.sub(r"'", ' ', entity)    #substitute ' in the entity by space
        entity = re.sub(r"\?", ' ', entity)   #substitute ? in the entity by space
        
        entity_tokens = entity.split()   # generate a list
        aa= entity_tokens[0].lower()
        
    
        
        list1 = ['0']*len(tokens)   # otherwise， IndexError: list assignment index out of range
        for j in range(0, len(tokens)):
            token_new = tokens[j].lower() 
            
    
            #print(token_new)
            
                
            for m in range(0, len(entity_tokens)):
                           
                if token_new == entity_tokens[m].lower():
                    
                    list1[j] = str(m+1)  #string
                else:
                    if list1[j] == '0':  #string
                        list1[j] = '0'   #string
    
                #print(entity_tokens[m].lower())    
        #print(list1)
        
        
        allnumbers = "".join(list1) # from list to string, eg, '0000000120000000', '000012300000000000000000000'
        #print(allnumbers)
        
        
        index_theory = ""  #empty string
        for q in range(0, len(entity_tokens)):
            index_theory = index_theory + str(q+1)  # a string, eg, '12', '123'
            
        try:
            location = allnumbers.index(index_theory)   # in the dataset 81 line: cognitive dissonance/self-perception processes, is a "bad case"
        except:
            #print("bad ones:", n)  #in a bad one, can't match theory in the sentence
            nn+=1
            bad.append(n)
            writer1.writerow([sentence, entity, n])
            continue
        
        
        list2 = ['O']*len(tokens)
        list2[location] = "B-TH"
        for t in range(0+1, len(entity_tokens)):
            list2[location+t] = "I-TH"
            
            
        for k in range(0, len(tokens)):  
            try:
                outfile.write(tokens[k]+'\t'+list2[k]+'\n')
            except:
                #continue
                outfile.write('NA'+'\t'+list2[k]+'\n')
                writer2.writerow([sentence, tokens[k]])
                
                #print("NA:", n)   #UnicodeEncodeError: 'charmap' codec can't encode character '\u0394' in position 0: character maps to <undefined>
        
        outfile.close()
        #don't forget ()
        
    else:
        #print("multi----------------------------:", n)
        count = 0
        try:
            span_list=[]
            for token in tokens:
                match_token = re.search(token, sentence, flags=re.I)
                span_list.append(match_token.span())
            
            location =['O']*len(span_list)  
            for entity in entity_multi:   #['attribution theory', 'self-determination theory', 'determinatio', 'self-determination']
                entity_tokens = entity.split(',')
                entity_tokens = "".join(entity_tokens)
                entity_tokens = re.sub(r'-+', ' ', entity_tokens)   #substitute - in the entity by space
                entity_tokens = re.sub(r"'", ' ', entity_tokens)    #substitute ' in the entity by space
                entity_tokens = re.sub(r"\?", ' ', entity_tokens)
                ruler=0
                
                entity_tokens = entity_tokens.split(' ')  # entity_tokens: ['self', 'determination']
                for etoken in entity_tokens:
                    ruler+=1
                    match_entity = re.search(etoken, sentence, flags=re.I)   #flags=re.IGNORECASE is the same
                    #print("entity:",match_entity.group()) 
                    #print("span:",match_entity.span()) 
                    if match_entity != None: 
                        for ss in range(0, len(span_list)):
                            if span_list[ss][0]==match_entity.span()[0]:
                                if ruler ==1:
                                    if location[ss] =="O":
                                        location[ss]="B-TH"
                                elif ruler > 1:
                                    if location[ss] =="O":
                                        location[ss]="I-TH"
            
            for kk in range(0, len(tokens)):  
                try:
                    outfile.write(tokens[kk]+'\t'+location[kk]+'\n')
                except:
                    #continue
                    outfile.write('NA'+'\t'+location[kk]+'\n')
            
            
            outfile.close()
        
        except:
            count+=1
            #print(lll)
            writer3.writerow([sentence, n, entity_multi])
            bad.append(n)
            nn+=1
            continue
        
        
        
        

memo1.close()  # not memo.close
memo2.close()
memo3.close()
    
print("total bad number:", nn)

#bad ones are 0 in size, remove all of them
for b in range(0, len(bad)):
    badfile = bad[b]
    path = os.path.join('D:\DARPAproject\\SBSpapers\\training_data_processing','all_txt_files',str(badfile)+'.txt')
    print(badfile,": deleted")
    
    os.remove(path)
    

print(count)
#============================================problem=========================================================
# sentence #81:
# It is therefore likely that these results reflect a wider change in norms relating to disposable carrier 
# bags in the UK, rather than being attributed to the policy itself or associated 
# cognitive dissonance/self-perception processes.

# dissonance/self-perception is recognized as 1 token, so can only recognize 'cognitive' in 'cognitive dissonance'

# allnumers is : 000000000000000000000000000000001000

# can't match '12', can't find theory 'cognitive dissonance' in this sentence
#======================================================================================================



#===========================================solution=====================================================
# sentence = re.sub(r'/+', ' ', sentence)  #substitute / in the sentence by space

# output: It is therefore likely that these results reflect a wider change in norms relating to 
# disposable carrier bags in the UK, rather than being attributed to the policy itself or associated 
# cognitive dissonance self-perception processes.
#======================================================================================================



#=============================================problem=========================================================
# bad ones: can't match entity to a token  in the sentence
    
# 994: Aggression-prevention initiatives require investments of an organization's limited financial, material, and human resources.   "aggression"
# 956: There were four measures of adjustment-aggression, prosocial behavior, internalizing problems, and depression.     "aggression"
# 944: However, it remains unknown whether this effect extends to the rejection-aggression link.      "aggression"
# 943: As such, the RAM model might not fully explain the rejection-aggression link.      "aggression"
# 890: Non-Aggression was positively related to theory of mind performance.    "aggression"
# 888: More precisely, retaliation seems like a form of affective aggression-which is immediate, emotional, and automaticand not a form of instrumental aggression-which is more deliberate (Geen, 2001).   "aggression"

# bad ones: 589: Figure 1 displays models of what I call collective identity-building intergroup violence, social identity-building intergroup violence, and intergroup violence as social control.    "social identity"
# bad ones: 596  Social-identity theory contends that a portion of one's self-concept is derived from perceived group membership (Turner and Oakes 1986;Gal 2015 offers a review).        "social identity"
# bad ones: 614  Further, while the ideal-types of collective and social identity-building intergroup violence offer conceptual traction to capture, compare, and contrast lynch mobs, typification is not explanation.
# bad ones: 627  Since group inclusion is contingent on acceptance by relevant others, social identity-building violence is a performance for peers to gain their approval and the group membership implied thereby.
# bad ones: 629
# bad ones: 656
# bad ones: 763


#===========================================solution=====================================================
# sentence = re.sub(r'-+', ' ', sentence)  #substitute / in the sentence by space

# entity = re.sub(r'-+', ' ', entity)
#======================================================================================================




#=============================================problem=========================================================
# bad ones: can't match entity to a token  in the sentence

# 29293: Changes in political institutions may increase the likelihood of bureaucratic purges (and therefore the degradation of state infrastructural power), though not necessarily, as in the process of institutional changes state 'legality may ensure the continuity of the state's normal administrative functions  such as keeping order, collecting taxes, running the courts, and so on'.
#        legality

# solution:
#     sentence = re.sub(r"'", ' ', sentence)    #substitute ' in the sentence by space
#======================================================================================================


#=============================================problem=========================================================
# 28797: For example, during the science track baccalaure´at exam, similarly to the HEC admission process, students have 
# to take written exams that include French literature ðboth written and oralÞ, mathematics, history, geography, 
# philosophy, and foreign languages ðoralÞ. 45 Hence, the comparison of the distributions of performances both at 
# the baccalaure´at exam and at the HEC admission contest provides a way of testing whether difference in ability 
# is a possible explanation for the differences in performances observed at the HEC admission contest.

# "in group and out group"

