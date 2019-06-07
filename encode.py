import os
from bitStream import BitStream
from huffmanTree import HuffmanTree


class Encoder:
    def __init__(self):
        self.tree = HuffmanTree()

    def encodeFile(self, fileName, outFileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = open(fileName, 'rb')
        writeFile = BitStream(outFileName, 'wb')
        c = readFile.read(1)
        while c:
            code = self.tree.encode(c[0])
            writeFile.write(code)
            c = readFile.read(1)
            # self.tree.printTree()
        writeFile.write(self.tree.endOfFile())
        readFile.close()
        writeFile.close()


if __name__ == '__main__':
    encoder = Encoder()
    encoder.encodeFile('./test.jpg', './code.txt')
