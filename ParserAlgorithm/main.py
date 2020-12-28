import re
from RecDescParser import RecDescParser

class Grammar:

    def __init__(self, file):
        self.__file = file
        self.__terminals = []
        self.__nonTerminals = []
        self.__productions = {}
        self.__startingSymbol = ''

        self.readGrammar()

    def getTerminals(self):
        return self.__terminals

    def getNonTerminals(self):
        return self.__nonTerminals

    def getProductions(self):
        return self.__productions

    def getProductionsForAGivenNonTerminal(self,nonterminal):
        if nonterminal not in self.__productions:
            return "There is no production for this nonterminal"
        else:
            return self.__productions[nonterminal]

    def getStartingSymbol(self):
        return self.__startingSymbol

    def add_values_in_dict(self,sample_dict, key, list_of_values):
        """Append multiple values to a key in the given dictionary"""
        if key not in sample_dict:
            sample_dict[key] = list()
        sample_dict[key].extend(list_of_values)
        return sample_dict

    def readGrammar(self):
        with open(self.__file, 'r', encoding="utf8") as reader:
            r=reader.read()
        text = r.split(";;")
        for i in range(0, len(text)):
            component = text[i]
            component = component.strip()
            component = re.sub(r'^.*?{{', '', component)
            component = re.sub(r'}}', '', component)

            component = component.split(',')
            if i == 0:
                for elem in component:


                    self.__nonTerminals.append(elem.strip())
            elif i == 1:
                for elem in component:
                    if elem == "space":
                        self.__terminals.append(" ")
                    else:
                        self.__terminals.append(elem.strip())
            elif i == 2:
                for elem in component:
                    transition = elem.split("->")
                    lhs = transition[0].strip()
                    rhs = transition[1].strip()
                    rhs = rhs.split("|")
                    print("rhs",rhs)
                    for i in rhs:
                        # if i not in self.__productions:
                        #     self.__productions[lhs] = list()
                        # # lhsProductions=self.__productions[lhs]
                        # # lhsProductions.append(i.strip())
                        # self.__productions = self.__productions[lhs].extend([i.strip()])
                        self.__productions = self.add_values_in_dict(self.__productions, lhs, [i.strip().split(" ")])
                        # print("self.__productions[lhs]",self.__productions[lhs])
                    # if lhs[1].strip() == "a-z":
                    #     for i in  list(string.ascii_lowercase):
                    #         self.__transitions[(lhs[0].strip(), i)] = rhs.strip()
                    # elif lhs[1].strip() == "A-Z":
                    #     for i in  list(string.ascii_uppercase):
                    #         self.__transitions[(lhs[0].strip(), i)] = rhs.strip()
                    # elif lhs[1].strip() == "1-9":
                    #     for i in range(1,9):
                    #         self.__transitions[(lhs[0].strip(), str(i))] = rhs.strip()
                    # else:
                    #     self.__transitions[(lhs[0].strip(), lhs[1].strip())] = rhs.strip()
            elif i == 3:
                self.__startingSymbol = component[0].strip()



def menu():
    gr = Grammar("Seminar7.txt")
    recDescParser= RecDescParser(gr)

    gr1 = Grammar("g2.txt")
    recDescParser1 = RecDescParser(gr1)

    while True:
        print("Choose a case")
        print("1.Display the nonterminals")
        print("2.Display the terminals")
        print("3.Display all the productions")
        print("4.Display the productions for a given nonterminal")
        print("5.Display the starting symbol")
        print("6.Verify if a sequence is accepted by the gr")
        print("7.Verify if a sequence is accepted by the gr(from file,seminar)")
        print("8.Verify if a sequence is accepted by the gr(from file,toy language)")
        print("9.Exit")
        case = input()
        if case == "1":
            print(gr1.getNonTerminals())
        elif case == "2":
            print(gr1.getTerminals())
        elif case == "3":
            print(gr1.getProductions())
            print(len(gr1.getProductions()))
        elif case == "4":
            nonterminal=input("Input a nonterminal:")
            print(gr1.getProductionsForAGivenNonTerminal(nonterminal))
            print(len(gr1.getProductionsForAGivenNonTerminal(nonterminal)))
        elif case == "5":
            print(gr1.getStartingSymbol())
        elif case == "6":
            sequence = input("Input a sequence:")
            recDescParser.parse(sequence)
        elif case == "7":
            f = open('seq.txt', "r")
            sequence = f.read()
            recDescParser.parse(sequence)
        elif case == "8":
            sequence=readFile()
            recDescParser1.parse(sequence)
        elif case == "9":
            break
        else:
            print("Invalid case")

def readFile():
    f = open('PIF.out', "r")
    finalSequence=""
    sequence = f.readlines()
    for i in sequence:
        aux = i.split("->")[0].strip()
        print("aux:",aux,"1")
        if aux != "":
            finalSequence+=aux
            finalSequence +=" "
    finalSequence = finalSequence.strip()
    print("finalSequence:",finalSequence)
    return finalSequence


menu()