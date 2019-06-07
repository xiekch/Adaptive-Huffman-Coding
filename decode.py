import os
from bitStream import BitStream
from huffmanTree import HuffmanTree


class Decoder:
    def __init__(self):
        self.tree = HuffmanTree()

    def decodeFile(self, fileName, outFileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = BitStream(fileName, 'rb')
        writeFile = open(outFileName, 'wb')
        running = True
        while True:
            char, running = self.tree.decode(readFile)
            if not running:
                break
            writeFile.write(char)
            # self.tree.printTree()

        readFile.close()
        writeFile.close()


if __name__ == '__main__':
    decoder = Decoder()
    decoder.decodeFile('./code.txt', './decode.txt')
