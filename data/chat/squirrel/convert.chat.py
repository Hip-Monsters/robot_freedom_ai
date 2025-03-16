  
corpus_out  = open("squirrel.chat.csv" , "w")     
tone_input  = open("./human_chat.txt", "r") 
i_res = 0 
corpus_out.write("actor,command,value\n")
 
for line in tone_input:   
    row        = line.split(":") 
    role       = row[0] 
    response   = row[1]   
    if role == "Human 1":
        role = "human" 
    else:
        role = "ai" 
    corpus_out.write(role + ',speak,"' + response +   '"\n')  
  