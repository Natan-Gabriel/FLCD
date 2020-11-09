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