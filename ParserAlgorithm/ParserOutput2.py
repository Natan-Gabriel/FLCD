class Node:
    def __init__(self, index, val, parent, sibling):
        self.index = index
        self.val = val
        self.parent = parent
        self.sibling = sibling

    def __str__(self):
        msg = "Node nr " + str(self.index) + " with value " + str(self.val)
        if self.parent:
            msg += ", parent " + str(self.parent)
        else:
            msg += ", no parent"
        if self.sibling:
            msg += " and sibling " + str(self.sibling)
        else:
            msg += " and no sibling. "
        return msg


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    def __str__(self):
        return self.data
        # return "self.data: "+self.data+"\n self.children"+str(self.children)
    def __repr__(self):
        return "self.data: "+self.data+"\n self.children"+str(self.children)


class Tree:
    def __init__(self,workingStack,grammar):
        self.workingStack=workingStack
        self.grammar = grammar
        self.current_index=1
        self.resultNodes=[]
        self.index=1
        self.queue=[]

    def constructTree(self):
        root = TreeNode(self.workingStack[0])
        self.constructTreeRecursively(root)
        self.parseTree(root)

    def constructTreeRecursively(self,node):
        data=node.data.split("_")
        prod=data[0]
        if(data[0]==node.data):
            prod_number=0
        else:
            prod_number = int(data[1])
        number_of_elements=len(self.grammar.getProductionsForAGivenNonTerminal(prod)[prod_number])

        while number_of_elements>0:
            if self.workingStack[self.current_index] in self.grammar.getTerminals():
                curr_elem=self.workingStack[self.current_index]
                new_node=TreeNode(curr_elem)
                node.children.append(new_node)
                number_of_elements -= 1
                self.current_index += 1
            else:
                curr_elem=self.workingStack[self.current_index]
                new_node=TreeNode(curr_elem)
                node.children.append(new_node)
                number_of_elements -= 1
                self.current_index += 1
                self.constructTreeRecursively(new_node)


    def parseTree(self,tree_node):  # kind of BFS algorithm
        dict={}

        new_node = Node(self.index, tree_node, None, None)
        dict[tree_node]=self.index
        self.index += 1
        self.resultNodes.append(new_node)
        self.queue.append(tree_node)

        while self.queue:
            tree_node=self.queue.pop(0)
            for i in range(len(tree_node.children)):
                #print("dict[tree_node]: ",dict[tree_node])
                if i>0:
                    new_node=Node(self.index,tree_node.children[i],dict[tree_node],self.index-1)
                else:
                    new_node = Node(self.index, tree_node.children[i], dict[tree_node], None)
                dict[tree_node.children[i]] = self.index
                self.index+=1
                self.resultNodes.append(new_node)
                if tree_node.children[i].data.split("_")[0] in self.grammar.getNonTerminals():
                    #print("HERE",tree_node.children[i].data.split("_")[0])
                    self.queue.append(tree_node.children[i])

    def printResult(self):
        length_list = [len(element) for row in self.resultNodes for element in [str(row.index),str(row.val),str(row.parent),str(row.sibling)]+['Index','Node','Father','Sibling'] if element!=None]
        column_width = max(length_list)

        row = "".join(element.ljust(column_width + 2) for element in
                      ['Index','Node','Father','Sibling'] if element != None)
        print(row)

        for row in self.resultNodes:
            row = "".join(element.ljust(column_width + 2) for element in [str(row.index),str(row.val),str(row.parent),str(row.sibling)] if element!=None)
            print(row)



