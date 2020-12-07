class Node:
    def __init__(self, index, val, father, sibling):
        self.index = index
        self.val = val
        self.father = father
        self.sibling = sibling

class ParserOutput:
    def __init__(self, grammar,seq):
        self.grammar=grammar
        self.seq=seq
        self.result=[]
        self.fathers=[]
        self.siblings=[]


    def getProductionStartingHere(self,node):
        result=[]
        prod = node.val.split("_")
        result.append(node.val)
        production=self.grammar.getProductionsForAGivenNonTerminal(prod[0])[prod[1]]

        for i in production.split("->")[1].split(" ").strip():
            if i in self.grammar.getTerminals():
                result.append(i)

            else:
                result.append(self.getProductionStartingHere(i))

        return result





    def constructTree(self,node):
        pass


    def printOutput(self):
        index=1
        for i in self.seq:

            if len(self.fathers)>0:
                if len(self.siblings)>0:
                    node = Node(index, i, self.fathers[-1], self.siblings[-1])
                    self.result.append(node)
                else:
                    node = Node(index, i, self.fathers[-1], -1)
                    self.result.append(node)
            else:
                node = Node(index, i, -1, -1)
                self.result.append(node)





            if i in self.grammar.getTerminals():
                self.siblings.append(i)

            if i in self.grammar.getNonTerminals():
                self.fathers.append(i)

            # node=Node(index, i, 0, 0)
            index+=1

    def printOutput2(self):
        index=1
        seq=self.seq
        for i in self.seq:

            if len(self.fathers)>0:
                if len(self.siblings)>0:
                    node = Node(index, i, self.fathers[-1], self.siblings[-1])
                    self.result.append(node)
                else:
                    node = Node(index, i, self.fathers[-1], -1)
                    self.result.append(node)
            else:
                node = Node(index, i, -1, -1)
                self.result.append(node)





            if i in self.grammar.getTerminals():
                node = Node(index, i, self.fathers[-1], self.siblings[-1])
                self.result.append(node)

                self.siblings.append(i)

            if i in self.grammar.getNonTerminals():
                seq.remove(self.getProductionStartingHere(i))
                node = Node(index, i, self.fathers[-1], self.siblings[-1])
                self.result.append(node)

                self.fathers.append(i)

            # node=Node(index, i, 0, 0)
            index+=1

