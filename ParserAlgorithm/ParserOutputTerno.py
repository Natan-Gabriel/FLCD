import copy

class Node:
    def __init__(self, index, val, parent, sibling):
        self.index = index
        self.val = val
        self.parent = parent
        self.sibling = sibling

    def __str__(self):
        msg = "Node nr " + str(self.index) + " with value " + str(self.val)
        if self.parent:
            msg += ", parent " + str(self.parent.val)
        else:
            msg += ", no parent"
        if self.sibling:
            msg += " and sibling " + str(self.sibling.val)
        else:
            msg += " and no sibling. "
        return msg

class ParserOutput:
    def __init__(self, grammar):
        self.grammar = grammar
        self.root = None
        self.index = 1
        self.nodes = []

    def build(self, workingStack):
        self.root = Node(self.index, workingStack[0], None, None)
        self.nodes.append(self.root)
        pending_prods = [(self.root, copy.deepcopy(self.grammar.getProductionsForAGivenNonTerminal(self.root.val)[0]))]
        while self.index < len(workingStack):
            splits = workingStack[self.index].split("_")
            if splits[0] in self.grammar.getNonTerminals():
                prod_nr = int(splits[1])
                new_node = Node(self.index+1, workingStack[self.index], pending_prods[-1][0], self.getSibling(pending_prods[-1][0]))
                self.nodes.append(new_node)
                pending_prods[-1][1].remove(splits[0])
                if len(pending_prods[-1][1]) == 0:
                    pending_prods.pop()
                pending_prods.append((new_node, copy.deepcopy(self.grammar.getProductionsForAGivenNonTerminal(splits[0])[prod_nr])))
            else:
                new_node = Node(self.index+1, workingStack[self.index], pending_prods[-1][0], self.getSibling(pending_prods[-1][0]))
                self.nodes.append(new_node)
                pending_prods[-1][1].remove(workingStack[self.index])
                if len(pending_prods[-1][1]) == 0:
                    pending_prods.pop()
            self.index+=1

    def getSibling(self, parent):
        siblings = []
        for i in self.nodes:
            if i.parent == parent:
                siblings.append(i)
        if len(siblings) == 0:
            siblings.append(None)
        return siblings[-1]

    def printOutput(self):
        for node in self.nodes:
            print(node)