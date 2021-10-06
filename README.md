
Step 1:
Use "load_json_sbs_find_claim_zone.py" to create the "sbs_sentences.json" file.  
It contains the sentences in each claim zone. This is input for step2.

Step 2:
USe "predict_sbs_in_claim_zone.py" to find the theory entities in the claim zone.

Need to create an virtual environment 'flair' with the following commands:  

conda create -n flair python=3.6  

conda activate flair  

pip install flair  


The model file folder 'resources' used in this script is in GOOGLE Drive. Need to download it and put in the same directory.
  
  
****************************************************************************************************************************
Currently not use simpletransformer

"simple_transformer_predict_paper.py" is used to find theory entities in papers.  
There are two parts, the first part is to segment a paper into sentences and the second part is to find the theory entities in each sentence. 

Have to download the folder 'outputs' and replace the path in the second part of simple_transformer_predict_paper.py.
