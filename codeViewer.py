import os
class Viewer:
    def __init__(self):
        pass    

    def view(self, fileName):
        if not os.path.exists(fileName):
            print('File doesnt exist.')
            return
        readFile = open(fileName, 'rb')
        for i in range(100):
            c = readFile.read(1)
            print(c)
        readFile.close()


if __name__ == '__main__':
    viewer=Viewer()
    viewer.view('./test.txt')
