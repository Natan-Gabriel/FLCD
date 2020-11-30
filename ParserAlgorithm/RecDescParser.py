class RecDescParser:

    def __init__(self, grammar):
        self.__s = "q"
        self.__i = 1
        self.__workingStack = []
        self.__inputStack = []
        self.__grammar = grammar


    def expand(self):
        elem = self.__inputStack.pop()
        self.__workingStack.append(elem)
        # self.__inputStack.append(self.__grammar.getProductionsForAGivenNonTerminal(elem)[0])
        self.__inputStack.extend(reversed(self.__grammar.getProductionsForAGivenNonTerminal(elem)[0]))

    def advance(self):
        self.__i += 1
        self.__workingStack.append(self.__inputStack.pop())

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
            self.__s="q"
            #self.__workingStack.append(self.__workingStack.pop())
            currIndex=listOfRHSProductions.index(self.__inputStack.pop())
            self.__inputStack.append(listOfRHSProductions[currIndex+1])
        else:
            if self.__i==1 and AJ==self.__grammar.getStartingSymbol():
                self.__s="e"
            else:
                self.__inputStack.pop()
                self.__inputStack.append(self.__workingStack.pop())

    def success(self):
        self.__s = "f"

    def parse(self, sequence):
        w = sequence.split()
        initialLength=len(sequence)
        self.__s = "q"
        self.__i = 1
        self.__workingStack = []
        self.__inputStack = [self.__grammar.getStartingSymbol()]
        while self.__s!="f" and self.__s!="e":
            if self.__s == "q":
                if len(self.__inputStack) == 0 and self.__i == initialLength+1:
                    self.success()
                    print("success")
                else:
                    if self.__inputStack[-1] in self.__grammar.getNonTerminals():

                        self.expand()
                        print("expand")
                        print("self.__workingStack: ", self.__workingStack)
                        print("self.__inputStack: " , self.__inputStack)
                    else:
                        if self.__inputStack[-1] == sequence[self.__i-1]:
                            self.advance()
                            print("advance")
                            print("self.__workingStack: ", self.__workingStack)
                            print("self.__inputStack: ", self.__inputStack)
                        else:
                            self.momentaryInsuccess()
                            print("momentaryInsuccess")
                            print("self.__workingStack: ", self.__workingStack)
                            print("self.__inputStack: ", self.__inputStack)
            else:
                if self.__s == "b":
                    if self.__workingStack[-1] in self.__grammar.getTerminals():
                        self.back()
                        print("back")
                        print("self.__workingStack: ", self.__workingStack)
                        print("self.__inputStack: ", self.__inputStack)
                    else:
                        self.anotherTry()
                        print("anotherTry")
                        print("self.__workingStack: ", self.__workingStack)
                        print("self.__inputStack: ", self.__inputStack)
        if self.__s == "e":
            print("ERROR")
        else:
            print("Accepted sequence")
            print(self.__workingStack)
            self.buildOutput()

    def buildOutput(self):
        output = ParserOutput(self.__grammar, self.__workingStack)
        output.printOutput()