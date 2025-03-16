 
import json  
import yake  
pyake = yake.KeywordExtractor(lan="en",n=3) 
corpus_out  = open("chat.initiate.json" , "w")     
tone_input  = open("./tone_v1.txt" )   

tones = set({})
tone_mapping = {}
tone_mapping["inspire"] = {}
tone_mapping["inspire"][""] = ""   
i_res = 0 
for line in tone_input:   
    row        = line.split("||") 
    response   = row[0]
    tone       = row[1].strip() 
    topics     = pyake.extract_keywords(response) 
    query      = "" 
    top        = ""
    i_rec     += 1
    for phrase, score in topics:
        top   = phrase
        if phrase.find(" ") == -1:
            query += phrase +  " "  

    dialogue = {"id": "tone."+ str(i_rec) ,
                   "query":query, 
                   "response":response, 
                   "tone":tone, 
                   "topics":topics} 
    corpus_out.write(json.dumps( dialogue) + "\n")  
  