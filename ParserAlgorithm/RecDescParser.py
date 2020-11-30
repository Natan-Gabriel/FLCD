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
        self.__inputStack.append(self.__grammar.getProductionsForAGivenNonTerminal(elem)[0])

    def advance(self):
        self.__i += 1
        self.__inputStack.append(self.__workingStack.pop())

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
            self.__workingStack.append(self.__workingStack.pop())
            self.__inputStack.append(self.__inputStack.pop())
        else:
            if self.__i==1 and AJ==self.__grammar.getStartingSymbol():
                self.__s="e"
            else:
                self.__workingStack.append(self.__inputStack.pop())

    def success(self):
        self.__s = "f"

    def parse(self, w):
        self.__inputStack.append(self.__grammar.getStartingSymbol)
        while self.__s!="f" and self.__s!="e":
            if self.__s == "q":
                if len(self.__inputStack) == 0 and self.__i == w:
                    self.success()
                else:
                    if self.__inputStack[-1] in self.__grammar.getNonTerminals():
                        self.expand()
                    else:
                        if self.__workingStack[-1] == w[self.__i-1]:
                            self.advance()
                        else:
                            self.momentaryInsuccess()
            else:
                if self.__s == "b":
                    if self.__workingStack[-1] in self.__grammar.getTerminals():
                        self.back()
                    else:
                        self.anotherTry()
        if self.__s == "e":
            print("ERROR")
        else:
            print("Accepted sequence")
            self.buildOutput()

    def buildOutput(self):
        output = ParserOutput(self.__grammar, self.__workingStack)
        output.printOutput()