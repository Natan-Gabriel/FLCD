from ParserOutputTerno import ParserOutput
from ParserOutput2  import Tree
import copy

class RecDescParser:

    def __init__(self, grammar,filename):
        self.__s = "q"
        self.__i = 1
        self.__workingStack = []
        self.__inputStack = []
        self.__grammar = grammar
        self.__filename = filename


    def expand(self):
        elem = self.__inputStack.pop(0)
        self.__workingStack.append(elem)
        # self.__inputStack.append(self.__grammar.getProductionsForAGivenNonTerminal(elem)[0])
        for i in reversed(self.__grammar.getProductionsForAGivenNonTerminal(elem)[0]):
            self.__inputStack.insert(0,i)

    def advance(self):
        self.__i += 1
        self.__workingStack.append(self.__inputStack.pop(0))

    def momentaryInsuccess(self):
        self.__s="b"

    def back(self):
        self.__i-=1
        a=self.__workingStack.pop()
        self.__inputStack.insert(0, a)

    def anotherTry(self):
        AJ=self.__workingStack[-1]
        deltaJ=self.__inputStack[0]

        AJ_splitted=AJ.split("_")
        currIndex=0
        if len(AJ_splitted)==2:
            currIndex=int(AJ_splitted[1])
        new_AJ=AJ_splitted[0]+"_"+str((currIndex+1))

        listOfRHSProductions=self.__grammar.getProductionsForAGivenNonTerminal(AJ_splitted[0])
        # print("listOfRHSProductions[currIndex]",currIndex,"",listOfRHSProductions[currIndex])
        # if type(listOfRHSProductions[currIndex]) is list:
        #     usedProduction = listOfRHSProductions[currIndex].copy()
        # else:
        #     usedProduction=[]
        usedProduction = listOfRHSProductions[currIndex].copy()
        if len(listOfRHSProductions)>currIndex+1:
            self.__s="q"
            while usedProduction!=[]:
                self.__inputStack.pop(0)
                usedProduction.pop(0)

            for i in reversed(listOfRHSProductions[currIndex+1]):
                self.__inputStack.insert(0, i)
            # self.__inputStack.insert(0,listOfRHSProductions[currIndex+1])
            self.__workingStack.pop()
            self.__workingStack.append(new_AJ)
        else:
            if self.__i==1 and AJ_splitted[0]==self.__grammar.getStartingSymbol():
                self.__s="e"
            else:
                while usedProduction != []:
                    self.__inputStack.pop(0)
                    usedProduction.pop(0)
                # self.__inputStack.pop()
                self.__workingStack.pop()
                self.__inputStack.insert(0,AJ_splitted[0])

    def success(self):
        self.__s = "f"


    def parse(self, sequence):
        # w = sequence.split()
        sequence = sequence.split(" ")
        print("sequence: ",sequence)
        # print("w: ",w)
        initialLength = len(sequence)
        self.__s = "q"
        self.__i = 1
        self.__workingStack = []
        self.__inputStack = [self.__grammar.getStartingSymbol()]
        while self.__s != "f" and self.__s != "e":
            if self.__s == "q":
                # print("len(self.__inputStack): ",len(self.__inputStack))
                # print("self.__i: ",self.__i)
                # print("initialLength: ",initialLength)
                if len(self.__inputStack) == 0 and self.__i == initialLength + 1:
                    self.success()
                    print("success")
                else:
                    # print(self.__inputStack[0],"aici",self.__inputStack[0] in self.__grammar.getNonTerminals())
                    if len(self.__inputStack) > 0 and self.__inputStack[0] in self.__grammar.getNonTerminals():

                        self.expand()
                        print("expand")
                        print("self.__workingStack: ", self.__workingStack)
                        print("self.__inputStack: ", self.__inputStack)
                    else:
                        if len(self.__inputStack) > 0 and self.__i - 1 < len(sequence) and self.__inputStack[0] == sequence[self.__i - 1]:
                            self.advance()
                            print("advance")
                            print("self.__workingStack: ", self.__workingStack)
                            print("self.__inputStack: ", self.__inputStack)
                        else:
                            self.momentaryInsuccess()
                            print("momentaryInsuccess")
                            print("self.__workingStack: ", self.__workingStack)
                            print("self.__inputStack: ", self.__inputStack)
            elif len(self.__workingStack) > 0:
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
            print("ERROR at index: " + str(self.__i))
        else:
            print("Accepted sequence")
            print(self.__workingStack)
            self.buildOutput()

    def buildOutput(self):
        # output = ParserOutput(self.__grammar)
        # output.build(self.__workingStack)
        # output.printOutput()

        output = Tree(copy.deepcopy(self.__workingStack),self.__grammar,self.__filename)
        output.constructTree()
        output.printResult()
        output.writeToFile()