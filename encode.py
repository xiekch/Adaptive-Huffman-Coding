import os
from bitStream import BitStream
from huffmanTree import HuffmanTree


class Encoder:
    def __init__(self):
        self.tree = HuffmanTree()
        pass

    def encodeFile(self, fileName,outFileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = open(fileName, 'rb')
        writeFile = open(outFileName, 'wb')
        c = readFile.read(1)
        while c:
            code = self.tree.encode(c[0])
            writeFile.write(code.encode())
            c = readFile.read(1)
            # self.tree.printTree()
        writeFile.write(self.tree.endOfFile().encode())
        readFile.close()
        writeFile.close()


if __name__ == '__main__':
    encoder = Encoder()
    encoder.encodeFile('./test.py','./code.txt')
