class Node:
    def __init__(self, char=None):
        self.weight = 0
        self.parent = None
        self.right = None
        self.left = None
        self.level = 0
        self.char=char

    def setLeft(self, node):
        self.left = node
        node.parent = self
        node.level = self.level+1

    def setRight(self, node):
        self.right = node
        node.parent = self
        node.level = self.level+1

    def replaceChild(self, child, node):
        if self.left == child:
            self.setLeft(node)
        elif self.right == child:
            self.setRight(node)

    def hasNoChild(self):
        return self.left == None and self.right == None

    def isAncestor(self, node):
        ancestor = self.parent
        while ancestor:
            if ancestor == node:
                return True
            ancestor = ancestor.parent
        return False

    def swap(self, node):
        if self == node or node.isAncestor(self) or self.isAncestor(node):
            return
        parent1 = self.parent
        parent2 = node.parent
        parent2.replaceChild(node, self)
        parent1.replaceChild(self, node)
