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

    def __str__(self):
        return str(self.__elems)


class SymbolTable:
    def __init__(self):
        self.__hashTable=HashTable(128)
    def pos(self,token):
        return self.__hashTable.add(token)
    def __str__(self):
        return str(self.__hashTable)







reservedWords=["char","int","string","boolean","array","for",
               "while","if","else","elif","of","program","read",
               "print"]
operators=["+","-","*","/","%","<","<=",">=",">","!=","=","==",
           "&&","||","!"]
separators=["(",")","[","]","{","}",";"," "]

tokens={}
file = open('token.in', 'r')
#print(file.read().splitlines())
for i in file.read().splitlines():
    x=i.split(" ")
    tokens[x[0]]=x[1]

print(tokens)

class PIF:
    def __init__(self):
        self.__pif={}
    def genPIF(self,token,index):
        self.__pif[token]=index
    def __str__(self):
        return str(self.__pif)

class Scanner():
    def __init__(self,filename):
        self.__st=SymbolTable()
        self.__pif=PIF()
        #self.__filename=filename
    def getST(self):
        return str(self.__st)
    def getPIF(self):
        return str(self.__pif)

    def getOperator(self,line,index): #look-ahead
        if ( index+1<len(line) ) and ( line[index] in operators ) and ( line[index+1] in operators ) and ( line[index]+line[index+1] in operators ):
            return tokens[line[index]+line[index+1]],line,index+2
        #elif ( index+1<len(line) ) and ( line[index] in separators ) and ( line[index+1] in separators ) and  ( line[index]+line[index+1] not in separators ):
        #    return line,index+1
        elif line[index] in operators:
            return tokens[line[index]],line,index+1
        elif ( index+1<len(line) ) and ( (line[index]+line[index+1]) in operators ):
            return tokens[line[index]+line[index+1]],line,index+2


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
                return tokens[word], line, index
        return tokens[word],line,index

    def getNumber(self, line, index):
        number = ""

        while len(line)>index and line[index]  in ["0","1","2","3","4","5","6","7","8","9"]:
            number += line[index]
            index += 1
        return number,line, index

    def getString(self,line,index):
        resultString=""
        # resultString="'"
        index+=1
        while len(line)>index and line[index]!='"':
            resultString+=line[index]
            index+=1
        return resultString,line,index

    def getIdentifier(self,line,index):
        resultIdentifier=""
        while len(line)>index and containsLettersOrDigits(line[index]):
            resultIdentifier += line[index]
            index += 1
        return resultIdentifier,line, index


    def getTokensByLine(self,line,linenumber):
        tokensInLine={}
        index=0
        while index<len(line):
            print("line")
            if line[index] in separators:  # is separator
                self.__pif.genPIF(line[index], 0)
                index+=1
            elif line[index] in operators or line[index] in ["&","|"]: #is operator
                token,line, index = self.getOperator(line, index)
                #tokensInLine[token]=self.__st.pos(token)
                self.__pif.genPIF(token, 0)
            elif self.isReservedWord(line,index): # is reserved word
                token,line,index = self.getReservedWord(line,index)
                #tokensInLine[token] = self.__st.pos(token)
                self.__pif.genPIF(token, 0)

            #now searching for constants and identifiers
            elif line[index]=='"':  #is steing constant
                token,line,index=self.getString(line,index)
                #tokensInLine[0] = self.__st.pos(token)
                ind=self.__st.pos(token)
                self.__pif.genPIF(token, ind)
            elif line[index] in ["0","1","2","3","4","5","6","7","8","9"]: #is numeric constant
                token,line,index=self.getNumber(line,index)
                #tokensInLine[0] = self.__st.pos(token)
                ind = self.__st.pos(token)
                self.__pif.genPIF(token, ind)
            elif containsLetters(line[index]) : #is identifier
                token,line, index = self.getIdentifier(line, index)
                #tokensInLine[1] = self.__st.pos(token)
                ind = self.__st.pos(token)
                self.__pif.genPIF(token, ind)
            else:
                print("Lexical error in line",linenumber,"starting at index",index)
        return tokensInLine

    def getTokens(self):
        lineNumber=1
        finalTokens={}
        f = open('p1.in', 'rb')
        for line in f.read().splitlines():
            self.getTokensByLine(line.decode("utf-8"),lineNumber)
            lineNumber+=1
        #print(finalTokens)



print("inceput")
scanner = Scanner('p1.in')

# print(scanner.getOperator('==',0)) #print 27
# print(scanner.getOperator('= = aaa',0)) #print 26
#
# print(scanner.getReservedWord('if ana',0)) #print 9
# print(scanner.getReservedWord('if for',3)) #print 7
#
# print(scanner.getIdentifier('iii ana',0)) #print 9
# print(scanner.getIdentifier('if frj',3)) #print 7
#
# print(scanner.getNumber("3333 aaa",0)) #print 9
# print(scanner.getNumber('if 222',3)) #print 7
#
# print(scanner.getString('"iii" ana',0)) #print 9
# print(scanner.getString('if "frj"',3)) #print 7
#
# #print(scanner.getTokensByLine('{[]}();== = >= for if "aaaa" 2345  if'))
# print(scanner.getTokensByLine('if(a>=b && a>=c){',1))
# print(scanner.getTokensByLine('print("the maximum number is a");',1))
# print(scanner.getTokensByLine('}',1))
# #print(scanner.getTokensByLine('int a=read ();'))


scanner.getTokens()
print("PIF: ",scanner.getPIF())
print("ST: ",scanner.getST())
print("final")
# file = open('p1.in', 'rb')
# for i in file.read().splitlines():
#     print(i.decode("utf-8") )
#
# print(tokens)






def test():
    hashTable = HashTable(128)
    print(hashTable.add(33))
    print(hashTable.add(4))
    print(hashTable.add(6))
    print(hashTable.add(5))
    print(hashTable.add(5))
    print(hashTable.add("ana"))
    print(hashTable.add("ana"))
    print(hashTable.add(0))
    print(hashTable.add(0))
    print(hashTable.add("7y"))



# test()
# # print('a' in ['a'-'z'])
# print(not re.search(r'[^a-zA-Z0-9. ]', 'ana'))




