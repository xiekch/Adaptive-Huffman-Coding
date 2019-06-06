from node import Node
from queue import Queue


class HuffmanTree:
    def __init__(self):
        self.root = Node()
        self.bytes = [None for i in range(256)]
        self.emptyNode = self.root

    def exist(self, char):
        return self.bytes[char] != None

    def addChar(self, char):
        node = Node(char)
        self.bytes[char] = node
        self.emptyNode.setLeft(Node())
        self.emptyNode.setRight(node)
        self.emptyNode = self.emptyNode.left

# encode
    def encode(self, char):
        if not self.exist(char):
            code = self.huffmanCode(self.emptyNode)
            code += '{0:08b}'.format(char)  # binary
            self.addChar(char)
        else:
            node = self.bytes[char]
            code = self.huffmanCode(node)

        self.updateTree(self.bytes[char])
        return code

    def endOfFile(self):
        return self.huffmanCode(self.emptyNode)

    def huffmanCode(self, node):
        code = ''
        if node == self.root:
            return '0'
        parent = node.parent
        while parent:
            if parent.left == node:
                code += '0'
            else:
                code +='1'
            node = parent
            parent = node.parent

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

    def updateTree(self, node):
        while node:
            node.swap(self.findFarthestNode(node.weight))
            node.weight += 1
            node = node.parent


# decode
    def decode(self, file):
        node = self.reHuffmanCode(file)
        if node == self.emptyNode:
            code = file.read(8)
            if code == '':
                return '', False
            # or end of the file
            char = int(code, 2)
            self.addChar(char)
        else:
            char = node.char
        self.updateTree(self.bytes[char])
        return char.to_bytes(1, byteorder='little'), True

    def reHuffmanCode(self, file):
        if self.root.hasNoChild():
            file.read(1)
            return self.root

        node = self.root
        while not node.hasNoChild():
            ch = file.read(1)
            if ch =='1':
                node = node.right
            elif ch == '0':
                node = node.left

        return node

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
            print('%s:%s' % (node.weight, chr(node.char or ord('*'))), end=' ')
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
        print('\n')
