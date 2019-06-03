import os
from bitStream import BitStream
from huffmanTree import HuffmanTree


class Encoder:
    def __init__(self):
        self.tree = HuffmanTree()
        pass

    def encodeFile(self, fileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = open(fileName, 'rb')
        writeFile = open('output.txt', 'w')
        c = readFile.read(1)
        # the first line is size of the file
        while c:
            code = self.tree.encode(c[0])
            writeFile.write(code+'\n')
            c = readFile.read(1)
            self.tree.printTree()
        readFile.close()
        writeFile.close()


if __name__ == '__main__':
    encoder = Encoder()
    encoder.encodeFile('./test.txt')
