import os
from bitStream import BitStream
from huffmanTree import HuffmanTree


class Encoder:
    def __init__(self):
        self.tree = HuffmanTree(1)

    def encodeFile(self, fileName, outFileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = open(fileName, 'rb')
        writeFile = BitStream(outFileName, 'wb')
        writeFile.write('{0:032b}'.format(os.stat(fileName).st_size))
        running = True
        while True:
            code, running = self.tree.encode(readFile)
            if not running:
                break
            writeFile.write(code)

        # writeFile.write(self.tree.endOfFile())
        self.tree.printTree()
        readFile.close()
        writeFile.close()


if __name__ == '__main__':
    encoder = Encoder()
    encoder.encodeFile('./test.txt', './code.txt')
