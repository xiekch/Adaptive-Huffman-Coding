from node import Node
from queue import Queue


class HuffmanTree:
    def __init__(self):
        self.root = Node(0)
        self.bytes = [None for i in range(256)]
        self.emptyNode = self.root

    def exist(self, char):
        return self.bytes[char] != None

    def addChar(self, char):
        node = Node(0)
        self.bytes[char] = node
        self.emptyNode.setLeft(Node(0))
        self.emptyNode.setRight(node)
        self.emptyNode = self.emptyNode.left

    def encode(self, char):
        code = self.getCode(char)
        if not self.exist(char):
            self.addChar(char)
        self.updateTree(self.bytes[char])
        return code

    def getCode(self, char):
        code = ''
        if not self.exist(char):
            while char:
                if char & 1:
                    code += '1'
                else:
                    code += '0'
                char = char >> 1
        else:
            node = self.bytes[char]
            while True:
                child = node
                node = node.parent
                if not node:
                    break
                if node.left == child:
                    code += '0'
                else:
                    code += '1'

        return code[::-1]  # reverse

    def findFarthestNode(self, weight):
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node.weight == weight:  # and node.hasNoChild():
                return node
            if node.right:
                q.put(node.right)
            if node.left:
                q.put(node.left)

    def swap(self, node1, node2):
        if node1 == node2 or node1.isAncestor(node2) or node2.isAncestor(node1):
            return
        parent1 = node1.parent
        parent2 = node2.parent
        parent2.replaceChild(node2, node1)
        parent1.replaceChild(node1, node2)

    def updateTree(self, node):
        while node:
            self.swap(node, self.findFarthestNode(node.weight))
            node.weight += 1
            node = node.parent

    def printTree(self):
        print('------tree------')
        q = Queue()
        q.put(self.root)
        level = 0
        while not q.empty():
            node = q.get()
            if node.level > level:
                level = node.level
                print()
            print('%s:%s' % (node.weight, node.level), end=' ')
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
        print('\n')
