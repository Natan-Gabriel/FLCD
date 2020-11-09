import re

import string

class FiniteAutomata:

    def __init__(self, file):
        self.__file = file
        self.__states = []
        self.__alphabet = []
        self.__transitions = {}
        self.__initialState = ''
        self.__finalStates = []
        self.classifyComponentsInFA()

    def getStates(self):
        return self.__states

    def getAlphabet(self):
        return self.__alphabet

    def getTransitions(self):
        return self.__transitions

    def getTransitionsAsString(self):
        string = ""
        for key in self.__transitions:
            string += "d(" + key[0] + "," + key[1] + ")=" + self.__transitions[key]+"\n"
        return string

    def getInitialState(self):
        return self.__initialState

    def getFinalStates(self):
        return self.__finalStates

    def classifyComponentsInFA(self):
        with open(self.__file, 'r') as reader:
            r=reader.read()
        text = r.split(";")
        for i in range(0, len(text)):
            component = text[i]
            component = component.strip()
            component = re.sub(r'^.*?{', '', component)
            component = re.sub(r'}', '', component)

            component = component.split(',')
            if i == 0:
                for elem in component:
                    self.__states.append(elem.strip())
            elif i == 1:
                for elem in component:
                    self.__alphabet.append(elem.strip())
            elif i == 2:
                for elem in component:
                    transition = elem.split("->")
                    lhs = transition[0]
                    rhs = transition[1]
                    lhs = lhs.split(":")
                    if lhs[1].strip() == "a-z":
                        for i in  list(string.ascii_lowercase):
                            self.__transitions[(lhs[0].strip(), i)] = rhs.strip()
                    elif lhs[1].strip() == "A-Z":
                        for i in  list(string.ascii_uppercase):
                            self.__transitions[(lhs[0].strip(), i)] = rhs.strip()
                    elif lhs[1].strip() == "1-9":
                        for i in range(1,9):
                            self.__transitions[(lhs[0].strip(), str(i))] = rhs.strip()
                    else:
                        self.__transitions[(lhs[0].strip(), lhs[1].strip())] = rhs.strip()
            elif i == 3:
                self.__initialState = component[0].strip()
            elif i == 4:
                for elem in component:
                    self.__finalStates.append(elem.strip())

    def isAccepted(self,string):
        currentState = self.__initialState
        for char in string:
            if (currentState, char) in self.__transitions:
                currentState = self.__transitions[(currentState, char)]
            else:
                return False
        if currentState in self.__finalStates:
            return True
        return False



def menu():
    fa = FiniteAutomata("FA.in")
    while True:
        print("Choose a case")
        print("1.Display the set of states")
        print("2.Display the alphabet")
        print("3.Display all the transitions")
        print("4.Display the initial state")
        print("5.Display the set of final states")
        print("6.Verify if a sequence is accepted by the FA")
        print("7.Exit")
        case = input()
        if case == "1":
            print(fa.getStates())
        elif case == "2":
            print(fa.getAlphabet())
        elif case == "3":
            print(fa.getTransitionsAsString())
        elif case == "4":
            print(fa.getInitialState())
        elif case == "5":
            print(fa.getFinalStates())
        elif case == "6":
            print("Input the sequence")
            sequence = input()
            print(fa.isAccepted(sequence))
        elif case == "7":
            break
        else:
            print("Invalid case")


menu()


faExample = FiniteAutomata("FA.in")
assert faExample.isAccepted("bbbbbbbaaaa") == True
assert faExample.isAccepted("bbbbbaaaa") == True
assert faExample.isAccepted("baaaaaaaa") == True
assert faExample.isAccepted("bbaaaaaaaa") == False
assert faExample.isAccepted("abbaaaaaaaa") == False
assert faExample.isAccepted("ababaaaaaaaa") == False



