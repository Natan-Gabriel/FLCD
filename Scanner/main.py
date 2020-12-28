import re

def containsLetters(s):
    return not re.search(r'[^a-zA-Z]', s)
def containsLettersOrDigits(s):
    return not re.search(r'[^a-zA-Z0-9]', s)

class HashTable:

    def __init__(self,length):
        self.__elems=[[] for i in range(length)]

    def getHashValue(self,elem):
        s=0
        if type(elem)!=str:
            elem=str(elem)
        for i in elem:
            s+=ord(i)
        return s%128

    def search(self,elem):
        hashValue=self.getHashValue(elem)
        if elem in self.__elems[hashValue]:
            return True
        else:
            return False


    def add(self,elem):
        hashValue = self.getHashValue(elem)
        currentList=self.__elems[hashValue]
        if len(currentList)==0:
            currentList=[]
            currentList.append(elem)
            self.__elems[hashValue]=currentList
            return (hashValue,0)
        elif self.search(elem)==False:
            currentList.append(elem)
            return (hashValue,len(currentList)-1)
        else: #the currentList is not empty and the element is present in the list
            return (hashValue,currentList.index(elem))

    # def __str__(self):
    #     return str(self.__elems)
    def __str__(self):
        resultString=""
        resultString += "Position in ST ->  Token  " + "\n"
        for i in range(0,len(self.__elems)):
            if self.__elems[i]!=[]:
                for j in range(0,len(self.__elems[i])):
                    resultString=resultString+"("+str(i)+","+str(j)+")"+"  ->  "+str(self.__elems[i][j])+"\n"
        return resultString




class SymbolTable:
    def __init__(self):
        self.__hashTable=HashTable(128)
    def pos(self,token):
        return self.__hashTable.add(token)
    def __str__(self):
        return str(self.__hashTable)


# Warning! Our scanner returns an lexical error if it finds undefined tokens:
# Pay attention and avoid usage of '“',tabs and comments in your programs!



reservedWords = ["char", "int", "string", "boolean", "array", "for",
                         "while", "if", "else", "elif", "of", "program", "read",
                         "print"]
operators = ["+", "-", "*", "/", "%", "<", "<=", ">=", ">", "!=", "=", "==",
                     "&&", "||", "!"]
extendedOperators = operators + ["&", "|"]
separators = ["(", ")", "[", "]", "{", "}", ";", " "]

digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

tokens = {}
file = open('token.in', 'r')
# print(file.read().splitlines())
for i in file.read().splitlines():
    x = i.split(" ")
    if x[0] == "space":
        tokens[' '] = x[1]
    else:
        tokens[x[0]] = x[1]


# print(tokens)
#
# print(");")
# print(")" in separators)
# print(";" in separators)

# Before and after:
# -constants:separators,operators;
# -identifiers:separators,operators;
# -reserved words:separators
# -operators:separators,constants,identifiers
# -separators:separators,operators,reserved words,constants,identifiers
#
# ?


class PIF:
    def __init__(self):
        self.__pif=[]
    def genPIF(self,token,index):
        self.__pif.append([token,index])
    # def __str__(self):
    #     return str(self.__pif)
    def __str__(self):
        resultString=""
        resultString += "Token Code  ->  Position in ST   "+"\n"
        for i in self.__pif:
            resultString+=str(i[0])+"  ->  "+str(i[1])+"\n"
        return resultString


class Scanner:
    def __init__(self,filename):
        self.__st=SymbolTable()
        self.__pif=PIF()
        self.__filename=filename


    def getST(self):
        return str(self.__st)
    def getPIF(self):
        return str(self.__pif)

    def isOperator(self,line,index): #look-ahead
        if ( index+1<len(line) ) and ( line[index] in operators ) and ( line[index+1] in operators ) and ( line[index]+line[index+1] in operators ):
            if (index+2==len(line)) or (line[index+2] in separators) or (line[index+2]=='"') or (line[index+2] in digits) or containsLetters(line[index+2]):
                return True
        elif line[index] in operators:
            if (index+1==len(line)) or (line[index+1] in separators) or (line[index+1]=='"') or (line[index+1] in digits) or containsLetters(line[index+1]):
                return True
        elif ( index+1<len(line) ) and ( (line[index]+line[index+1]) in operators ):
            if (index + 2 == len(line)) or (line[index + 2] in separators) or (line[index + 2] == '"') or (line[index + 2] in digits) or containsLetters(line[index + 2]):
                return True
        return False

    def getOperator(self,line,index): #look-ahead
        if ( index+1<len(line) ) and ( line[index] in operators ) and ( line[index+1] in operators ) and ( line[index]+line[index+1] in operators ):
            return line[index]+line[index+1],line,index+2
        #elif ( index+1<len(line) ) and ( line[index] in separators ) and ( line[index+1] in separators ) and  ( line[index]+line[index+1] not in separators ):
        #    return line,index+1
        elif line[index] in operators:
            return line[index],line,index+1
        elif ( index+1<len(line) ) and ( (line[index]+line[index+1]) in operators ):
            return line[index]+line[index+1],line,index+2


    def isReservedWord(self,line,index):
        word=""
        while len(line)>index and line[index] not in separators:
            word+=line[index]
            index+=1
            if word in reservedWords:
                return True
        return False


    def getReservedWord(self,line,index):
        word=""
        while len(line)>index and (line[index] not in separators):
            word+=line[index]
            index+=1
            if word in reservedWords:
                return word, line, index
        return word,line,index


    def isNumber(self, line, index):
        while len(line)>index and line[index]  in ["0","1","2","3","4","5","6","7","8","9"]:
            index += 1
        if (len(line)==index) or (line[index] in separators) or (line[index] in operators):
            return True
        return False


    def getNumber(self, line, index):
        number = ""

        while len(line)>index and line[index]  in ["0","1","2","3","4","5","6","7","8","9"]:
            number += line[index]
            index += 1
        return number,line, index


    def isString(self,line,index):
        index+=1
        while len(line)>index:
            if line[index]=='"':
                if (len(line) == index + 1) or (line[index + 1] in separators) or (line[index + 1] in operators):
                    return True
            index+=1
        return False

    def getString(self,line,index):
        resultString=""
        # resultString="'"
        index+=1
        while len(line)>index and line[index]!='"':
            resultString+=line[index]
            index+=1
        if len(line)>index and line[index]=='"':
            index+=1
        return resultString,line,index

    def isIdentifier(self,line,index):
        while len(line)>index and containsLettersOrDigits(line[index]):
            index += 1
        if (len(line)==index) or (line[index] in separators) or (line[index] in operators):
            return True
        return False

    def getIdentifier(self,line,index):
        resultIdentifier=""
        while len(line)>index and containsLettersOrDigits(line[index]):
            resultIdentifier += line[index]
            index += 1
        return resultIdentifier,line, index

    def getErrorToken(self,line,index):
        resultString=""
        while len(line)>index and (line[index] not in separators): #and (line[index] not in operators):
            resultString+=line[index]
            index+=1
        return resultString

    def getTokensByLine(self,line,linenumber):
        #tokensInLine={}
        index=0
        while index<len(line):
            #print("line")
            if line[index] in separators:  # is separator
                self.__pif.genPIF(line[index], 0) #self.__pif.genPIF(tokens[line[index]], 0)
                #print("adding "+line[index] +" to separators")
                index+=1
            elif line[index] in extendedOperators and self.isOperator(line,index): #is operator
                token,line, index = self.getOperator(line, index)
                #tokensInLine[token]=self.__st.pos(token)
                self.__pif.genPIF(token, 0)
            elif self.isReservedWord(line,index): # is reserved word
                token,line,index = self.getReservedWord(line,index)
                #tokensInLine[token] = self.__st.pos(token)
                self.__pif.genPIF(token, 0)


            #now searching for constants and identifiers
            elif line[index]=='"' and self.isString(line,index):  #is string constant
                token,line,index=self.getString(line,index)
                #tokensInLine[0] = self.__st.pos(token)
                ind=self.__st.pos(token)
                self.__pif.genPIF(tokens['Constant'], ind)
            elif line[index] in digits and self.isNumber(line,index): #is numeric constant
                token,line,index=self.getNumber(line,index)
                #tokensInLine[0] = self.__st.pos(token)
                ind = self.__st.pos(token)
                self.__pif.genPIF(tokens['Constant'], ind)
            elif containsLetters(line[index]) and self.isIdentifier(line,index) : #is identifier
                token,line, index = self.getIdentifier(line, index)
                #tokensInLine[1] = self.__st.pos(token)
                ind = self.__st.pos(token)
                self.__pif.genPIF(tokens['Identifier'], ind)
            else:
                errorToken=self.getErrorToken(line,index)
                return -1,linenumber,index,errorToken
        return 1,1,1,1
        #return tokensInLine

    def getTokens(self):
        lineNumber=1
        finalTokens={}
        f = open(self.__filename, 'rb')
        for line in f.read().splitlines():
            res,linenumber,index,errorToken=self.getTokensByLine(line.decode("utf-8"),lineNumber)
            if res==-1:
                print("Lexical error in line "+str(linenumber)+",starting at index "+str(index)+".The token is: "+str(errorToken))
                return
            lineNumber+=1
        #print(finalTokens)
        print("The program is lexically correct")
        f.close()
        f = open("PIF.out", "w")
        f.write(self.getPIF())
        f.close()
        f = open("ST.out", "w")
        message = "I have a unique symbol table for identifiers and constants,represented as a hash table\n"
        f.write(message+self.getST())
        f.close()



scanner = Scanner('p3.in')
scanner.getTokens()
print("PIF: ",scanner.getPIF())
print("ST: ",scanner.getST())



