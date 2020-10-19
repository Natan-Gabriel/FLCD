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



class SymbolTable:
    def __init__(self):
        self.__hashTable=HashTable(128)
    def pos(self,token):
        return self.__hashTable.add(token)



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



test()








