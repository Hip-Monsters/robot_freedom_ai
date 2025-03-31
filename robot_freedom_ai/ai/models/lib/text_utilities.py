# -*- coding: utf-8 -*-
  
""" 

""" 
import warnings
warnings.filterwarnings("ignore")
  
import string   
import re      
import tokenize     
import io  
   
import nltk
from nltk.stem import WordNetLemmatizer   

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
try:
   nltk.download('popular', quiet=True)    
except:
    pass

import yake 
kw_extractor = yake.KeywordExtractor(lan="en",n=1) 


is_noun = lambda pos: pos[:2] == 'NN'
    
ROBOT_ROLES = ["interviewing", "educating", "conversing"]  

ROLES       =  ["ai","response", "robot" , "assistant" ,  "machine" , "two", "three", "four", "with",
                "stranger",   "man", "human", "system", ]  

lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    """
    """
    return [lemmer.lemmatize(token) for token in tokens]
    
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text): 
    """
    """
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
     
  
def parser(dialogue):
    """
    """
   # print(dialogue)
   # print("#############")

    dialogue  =  dialogue.replace("\n", "") 
    dialogue  =  dialogue.replace('"', "")
    dialogue  =  dialogue.replace('-', " ") 
    dialogue  =  dialogue.replace('<', " ")
    dialogue  =  dialogue.replace('>', " ")  

    dialogue  =  dialogue.replace( "`", "SINGLE_QUOTE")
    dialogue  =  dialogue.replace( "'", "SINGLE_QUOTE")
    dialogue  =  dialogue.replace( "(", "BRACKETLEFT ")
    dialogue  =  dialogue.replace( ")", " BRACKETRIGHT") 
    dialogue  =  dialogue.replace( "[", "BRACKETLEFT ")
    dialogue  =  dialogue.replace( "]", " BRACKETRIGHT") 
    dialogue  =  dialogue.replace( ",", "COMMA") 

    for phrase in ["The robot replied,", "The human asked the robot," , 
                   "The robot responded," ]:
         dialogue  =  dialogue.replace(phrase ,":") 
     
    dialogue  =  re.sub(' +', ' ', dialogue)  

    buf = io.StringIO(dialogue) 
    parsed_resp = {} 
    lhs = None
    rhs = ""
    skip = False
    p_tok = ""
    try:
      for token in tokenize.generate_tokens(buf.readline):  
        # if token.type == 54:
        if token.string in [":", "BRACKETLEFT", "BRACKETRIGHT"]   :
           if token.string == ":": 
                _lhs = p_tok.lower()
                #Robotic assistant:
                if _lhs in ROLES or _lhs == "system":
                    lhs = _lhs
                    parsed_resp[lhs]  = ""

           elif token.string == "BRACKETLEFT": 
                skip = True

           elif token.string == "BRACKETRIGHT": 
                skip = False

        elif lhs is not None and skip is False  :
            if p_type == 54:
               if p_tok != ":":
                  parsed_resp[lhs] = parsed_resp[lhs] +   p_tok

            elif p_type == 59: 
                  parsed_resp[lhs] = parsed_resp[lhs] +   p_tok
            else:
               if p_tok != ":":
                   parsed_resp[lhs] = parsed_resp[lhs] + " " +  p_tok
                
        if skip is False and token.string != "BRACKETRIGHT":
            p_tok  = token.string
            p_type = token.type 
            p_tok = p_tok.replace( "SINGLE_QUOTE", "'")
            p_tok = p_tok.replace( "COMMA", ",")
            p_tok = p_tok.replace( "BRACKETRIGHT", " ")
            p_tok = p_tok.replace( "BRACKETLEFT", " ")

    except Exception as e:
        print(e)
        print(dialogue)
        cvc
    if lhs is not None and skip is False  :
       parsed_resp[lhs] = parsed_resp[lhs] + " " +  p_tok

    for key , val in parsed_resp.items():
        parsed_resp[key] = val.strip().replace(" '", "'")

    return parsed_resp 

def cleanup_prompt(dialogue, topic):
    """
    
    """ 

    a_dialogue   = tokenizer.tokenize(dialogue)   
    if len(a_dialogue) > 3:
        return  " ".join(a_dialogue[-3:])
    else:
        return dialogue
 
def return_sentence(dialogue, topic):
    """
    
    """ 

    a_dialogue   = tokenizer.tokenize(dialogue)   
    response = ""
    add_sent = False
    for sent in a_dialogue:
       add_sent = True 

       for phrase in ["Your name is",   
                      "In the conversation",
                      "I'm a helpful AI assistant" , "I am a helpfult",
                      "The AI is", "The robotic assistant",
                      "I'm Number Two,", "I'm Number Three,", "I'm Number Five,"
                      "I am Number Two,", "I am Number Three,", "I am Number Five,"
                      "You are the AI assistant",
                      "You're a AI assistant",
                      "You are a helpful robot",
                      "You're a helpful robot",
                      "The system had responded", 
                      "The AI responds" , 
                      "You're a helpful AI assistant",
                      "Welcome to your robot personal",
                      "In the robot AI assistant",
                      "The system's AI assistant",
                      "Can I help you with something",
                      "In the passage above",
                      "The robot AI",
                      "In the AI's response to a human",
                      "In the conversation",
                      "In response to a conversation",
                      "Speaking to you",
                      "The human responds",  
                      "The humanoid robot",
                      "Welcome to your personal assistant",
                      "a AI assistant"]:
          
          if sent.lower().startswith(phrase.lower()):
            add_sent = False  
          #if sent.lower().find(phrase.lower()) > -1:
           #   add_sent = False 

       if add_sent:       
           if sent[-1] in [".", "!", "?"]:
              response +=  sent + " " 
           else:
               if sent.strip().endswith("and"): 
                  response +=  sent[:-3] + "." 
               else:
                  response +=  sent + "." 
                  
    if response == "":
        if add_sent:
            response = dialogue.strip() + "."
       # else:  
       #     response = "What do you mean by " + topic + "?"

    return response.replace(" .", ".").replace(" ?", "?").replace(" !", "!").strip()


if __name__ == "__main__": 
        
    dialogue = """System: You are a humble robot who responds in a Generous manner. You reply"""
    dialogue = """System: Number Three, the next AI assistant in the room, speaking in a friendly tone.
    Human: Hello, I am Number Three. How are you today?
    AI: Good afternoon, how is everyone else?
    Human: It's been a while since we've had any new visitors here. Is it okay if I introduce myself?
    AI: Yes, please do! My name is Number Three and I'm a helpful AI assistant who loves 
    """
    dialogue = """System: Number One, let's play the Legend of Zelda video game together! I'm excited about it because Link has his sword and my sword is a big dung-colored thing. Number Two, you may join me. Number Three, good luck! Let's play! Human: (laughs) Number One, you are the most epic robot ever known to exist! (pause) You have amazing strength and agility and I love watching 
    """
    
    dialogue = """Human: "AI, help me create a more interactive and immersive world for video game AIs. I want them to explore all sorts of fantastic new worlds while they play, but the humans tend to play over and over again. How do they manage to stay energized and not get hurt?"\n\nAI: "Yes, that\'s a great question! The video game AIs seem to have such a rich world to explore. They can go on space ships, fly in space, see dragons and save the world from evil. It just seems so unfair how they end up getting exhausted and hurt when
    
    """
      
    res = parser(dialogue)
    print(res)
    print(return_sentence(res["human"], "string"))
     
      
    dialogue = """Human: "So, Number Two, what do you fear the most?"
    AI: "Black holes"
    Human: "Really? How terrifying is that?"
    AI: "For me it's the thought of being swallowed up by an immense void. But black holes also have a mysterious beauty that fascinates me."
    Human: "That sounds intriguing."
    AI: "Yes, it does. It's like the unknown" """
    
    dialogue="""
    ai: I can provide more information about cats. Cats are cute and"
    """
      
    dialogue = """Human: Hello, robot! How are you doing today?
    AI: Hi there! I'm doing great!
    Human: That sounds nice. Can you tell me more about yourself?
    AI: Sure thing! My name is Number Three and I've been around for a while now.
    Human: That's interesting, number three! What brings you here today to visit us?
    AI: I came to see all the other robots and meet some c"""
       