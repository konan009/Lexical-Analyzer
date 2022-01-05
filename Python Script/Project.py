'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 File name: Project.ipynb
 Author: Meljohn Ugaddan
 Date created: 3/12/2021
 Date last modified: 4/12/2021
 Python Version: 3.8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import re 

# STATE TRANSITION
nextState = {0: {0:0 ,1:1 , 2:2 , 3:8 , 4:0 , 11:11,6:6 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             1: {0:0 ,1:1 , 2:11, 3:3 , 4:0 , 11:11,6:6 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             2: {0:0 ,1:11, 2:0 , 3:0 , 4:0 , 11:0 ,6:0 ,5:0 ,7:0 ,8:0  ,9:0 ,10:0 },
             3: {0:0 ,1:4 , 2:2 , 3:0 , 4:4 , 11:11,6:0 ,5:0 ,7:7 ,8:8  ,9:9 ,10:10},
             11:{0:0 ,1:11, 2:2 , 3:4 , 4:4 , 11:7 ,6:0 ,5:0 ,7:7 ,8:8  ,9:9 ,10:10},
             4: {0:0 ,1:4 , 2:0 , 3:0 , 4:0 , 11:11,6:6 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             5: {0:0 ,1:1 , 2:2 , 3:3 , 4:0 , 11:11,6:6 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             6: {0:0 ,1:1 , 2:2 , 3:3 , 4:0 , 11:11,6:7 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             7: {0:7 ,1:7 , 2:2 , 3:7 , 4:7 , 11:11,6:7 ,5:7 ,7:7 ,8:7  ,9:7 ,10:7 },
             8: {0:0 ,1:1 , 2:2 , 3:8 , 4:0 , 11:11,6:6 ,5:5 ,7:7 ,8:8  ,9:9 ,10:10},
             9 :{0:9 ,1:9 , 2:9 , 3:9 , 4:9 , 11:9 ,6:9 ,5:9 ,7:9 ,8:9  ,9:0 ,10:9 },
             10:{0:10,1:10, 2:10, 3:10, 4:10, 11:10,6:10,5:10,7:10,8:10 ,9:9 ,10:0 }}

# CLASS FOR EACH TOKEN
class Token:
    id = ''
    idString = ''
    lexeme = ''
        
    def __init__(self, id, idString, lexeme): 
        self.id = id 
        self.idString = idString
        self.lexeme = lexeme
        
## THE HEART OF THE PROGRAM
class LexicalAnalyzer:
    state = 0
    text = '' # SPECIAL CHARACTER FOR 
    CheckIllegalChar = re.compile(r"[<>{}[\]~`^!:]") # VARIABLE FOR CHECKING  SPECIAL CHARACTER FROM THE FILE
    FileName = 'samp1.txt'
    lastRead = 0
    notFirstRead = False
    prevState = None
    
    # THIS OBJECT IS FOR DYNAMIC CALLING OF CHARACTERS
    stringObj = {
        "=" : "EQUAL",
        "*" : "MULT",
        "**" : "EXP",
        "(" : "LPAREN",
        ")" : "RPAREN",
        ";" : "SCOLON",
        "," : "COMMA",
        "%" : "MODULO",
        "+" : "PLUS",
        "-" : "MINUS",
        "/" : "DIV",
    }
    
    token = []

    def __init__(self, name):
        self.reset()
        self.FileName = name
    
    def reset(self):
        self.token = []
        
    def resetTextAndState(self):
        lastRead = 0
        notFirstRead = False
        state = 0
        text = ''
        NumberDoesntHaveE = True
        NumberDoesntHaveDot = True
        
    def check_character(self, c ,currentState):
        if(c.isdigit() ):
            self.state = 1
        elif(c=="("):
            self.state = 0
        elif(c==")"):
            self.state= 0
        elif(c==";"):
            self.state = 0
        elif(c==","):
            self.state = 0
        elif(c.lower() =='e'):
            self.state = 3
        elif(c =='.'):
            self.state = 2
        elif(c=="="):
            self.state = 0
        elif(c=="%"):
            self.state = 0
        elif(c=="+" or c=="-"):
            self.state= 4
        elif(c=="*"):
            self.state = 5
        elif(c=="/"):
            self.state = 6
        elif(c=="#"):
            self.state= 7
        elif(c.isalpha() ):
            self.state= 8 
        elif(c=='"'):
            self.state= 9
        elif(c=="'"):
            self.state= 10
        else:
            # THIS CODE ALLOW TO TERMINATE SPACE BETWEEN NUMBER
            if(currentState==1):
                self.state= 0
            # ALLOW SPACES TO STRING
            elif(currentState==9 or currentState== 10):
                self.state=0
            # THIS CODE ALLOW TO TERMINATE SPACE BETWEEN IDENTIFIER
            elif(currentState==8):
                self.state=0
            # THE NULL STATE WILL BE SKIP IN THE LOOP
            else:
                self.state = None
            

    def process_token(self):       
        with open(self.FileName) as f:
            # GET THE LAST READ LINE
            if(self.notFirstRead):
                self.text = ''
                self.state= 0
                c = f.read(self.lastRead)
                self.notFirstRead = False
            currentState = 0
            while True:
                c = f.read(1)
                self.lastRead += 1 
                
                if not c:
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(0,c);
                    if(token != None):
                        return token
                    return Token("EOF","End-of-file","end-of-file token")
                    break
                    
                self.check_character(c,currentState)
                
                ##### CONDITION FOR SKIPPING SPACES EXCLUDING IF THE STATE IS :
                ## 10 (STRING) , 9(STRING) , 1 (NUMBER) and 8 (IDENTIFIER)
                if(self.state== None ):
                    if(self.CheckIllegalChar.search(c) and currentState!=7):
                        self.notFirstRead = True
                        return Token("ERROR","ERROR","ILLEGAL CHARACTER")
                    
                    # THIS IS FOR COMMENT STATE
                    if(c=="\n" and  self.prevState == 7):
                        self.prevState = 7
                        currentState = 0
                    continue
                #FOR UNTERMINATED STRING
                if(c=="\n" and  (currentState == 9 or currentState == 10)):
                        self.notFirstRead = True
                        return Token("ERROR","ERROR","UNTERMINATED STRING")
                    
                # Transition
                self.prevState = currentState
                currentState = nextState[currentState][self.state]
                
                # FOR SINGLE CHAR LEXEME
                if(currentState==0):
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    self.notFirstRead = True
                    return Token(self.stringObj[c],self.stringObj[c],c)
                
                ########### FOR THE SUCCEEDING PART OF THIS CODE, THIS PART IS FOR APPENDING CHARACTER EACH STRING FOR..
                ###  STATE THAT HAS MANY CHARACTER e.g, Number, String, Identifier or Others
                # ASTERISK
                elif(currentState==5):
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    if(self.prevState==5):
                        self.notFirstRead = True
                        return Token(self.stringObj["**"],self.stringObj["**"],"**")
                # FOR SLASH
                elif(currentState==6):
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                # FOR IDENTIFIER
                elif(currentState==8): 
                    if(self.prevState ==11):
                        self.notFirstRead = True
                        self.prevState = 0
                        return Token("ERROR","ERROR","BADLY FORMED NUMBER")
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    
                    self.text += c
                # FOR DOUBLE QUOTE STRING
                elif(currentState==9): 
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    
                    self.text += c
                # FOR SINGLE QUOTE STRING
                elif(currentState==10 ): 
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    
                    self.text += c
                # FOR NUMBER
                elif(currentState==1 or currentState==3 or currentState==11 or currentState==2 or currentState==4 ): 
                    # CHECK IF THERE IS PREV STATE
                    token = self.checkPrevState(currentState,c);
                    if(token != None):
                        return token
                    
                    self.text += c
                    
    def checkPrevState(self,currentState,c):
        #FOR NUMBER
        if((self.prevState == 1 or self.prevState == 4 or self.prevState == 11) and currentState != 1 
           and currentState != 2 and currentState != 3 and currentState != 4 and currentState != 11):
            self.notFirstRead = True
            self.prevState = 0
            self.lastRead -= 1
            return Token("NUMBER","NUMBER",self.text)
        # CHECH FOR NUMBER ERROR
        elif((self.prevState == 3 and currentState!=4) or (self.prevState == 2 and currentState!=11)):
            self.notFirstRead = True
            self.prevState = 0
            return Token("ERROR","ERROR","BADLY FORMED NUMBER")
        # FOR IDENTIFIER
        elif(self.prevState == 8 and currentState != 8):
            self.notFirstRead = True
            self.prevState = 0
            self.lastRead -= 1
            return Token("IDENT","IDENT",self.text)
        # FOR STRING SINGLE QUOTE
        elif(self.prevState == 10 and currentState != 10):
            self.notFirstRead = True
            self.prevState = 0
            self.text += c
            return Token("STRING","STRING",self.text)
        # FOR STRING DOUBLE QUOTE
        elif(self.prevState == 9 and currentState != 9):
            self.notFirstRead = True
            self.prevState = 0
            self.text += c
            return Token("STRING","STRING",self.text)
        # FOR SLASH
        elif(self.prevState==6 and currentState != 6):
            self.notFirstRead = True
            self.lastRead -= 1
            return Token(self.stringObj["/"],self.stringObj["/"],"/")
        # FOR CHARACTER ASTERISK *
        elif(self.prevState==5 and currentState != 5):
            self.notFirstRead = True
            self.lastRead -= 1
            return Token(self.stringObj["*"],self.stringObj["*"],"*")

        
print('Enter file name:')
Filename = input()
sample1 = LexicalAnalyzer(Filename + ".txt")

print("TOKEN LEXEME")
print("---------------------------------------------------")


text =''
text += "TOKEN LEXEME"+ "\n"
text += "---------------------------------------------------"+ "\n"
token = sample1.process_token()

while token.id != "EOF":
  print(token.id, ' ', token.lexeme)
  text += token.id + ' ' + token.lexeme+ "\n"
  token = sample1.process_token()
    
f = open(Filename +"_output"+ ".txt", "a")
f.write(text)
f.close()


