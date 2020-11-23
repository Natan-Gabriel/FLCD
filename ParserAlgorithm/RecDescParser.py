class RecDescParser:

    def __init__(self, grammar):
        self.__s = "q"
        self.__i = 1
        self.__workingStack = []
        self.__inputStack = []
        self.__grammar = grammar


    def expand(self):
        elem = self.__inputStack.pop(0)
        self.__workingStack.insert(0, elem)
        self.__inputStack.insert(0, self.__grammar.getProductionsForAGivenNonTerminal(elem)[0])

    def advance(self):
        self.__i += 1
        self.__inputStack.insert(0, self.__workingStack.pop(0))

    def momentaryInsuccess(self):
        self.__s="b"

    def back(self):
        self.__i-=1
        a=self.__workingStack.pop()
        self.__inputStack.append(a)

    def anotherTry(self):
        AJ=self.__workingStack[-1]
        deltaJ=self.__inputStack[-1]

        listOfRHSProductions=self.__grammar.getProductionsForAGivenNonTerminal(AJ)
        if listOfRHSProductions[-1]!=deltaJ:
            index=listOfRHSProductions.index(deltaJ)
            self.__s="q"
            AJ=self.__workingStack.pop()
            self.__workingStack.add(AJ)
            deltaJ = self.__inputStack.pop()
            self.__inputStack.add(deltaJ)
        else:
            if self.__i==1 and AJ==self.__grammar.getStartingSymbol():
                self.__s="e"
            else:
                AJ=self.__inputStack.pop()
                #self.__workingStack.pop()
                self.__workingStack.add(AJ)





    def success(self):
        self.__s = "f"



