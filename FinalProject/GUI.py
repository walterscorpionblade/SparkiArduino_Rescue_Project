# CSCI3302 FINAL PROJECT
#Team member: Xinyang Yuan, Zijun Liu, Ruitong Sun

from tkinter import *
import random
import time
import bluetooth

import queue

class BlueTooth:
    def __init__(self, addr = "98:D3:31:FC:46:BF"):
        self.bd_addr = addr
        self.port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.bd_addr, self.port))
    # We specified that every message is ended with a '#'

    def sendMessage(self, string):
        print("send " + str(string))
        self.sock.send(string)
        self.sock.send('#')

    def recvMessage(self):

        ret = ''
        ss = self.sock.recv(1000)
        for ch in ss:
            ret = ret + str(chr(ch))
        while (ret[-1] != '#'):
            ss = self.sock.recv(1000)
            for ch in ss:
                ret = ret + str(chr(ch))
        print("revc = " + str(ret))
        return str(ret[0:-1])

    def test(self):
        while True:
            data = input()
            if len(data) == 0:
                break
            self.sendMessage(str(data))
            ss = self.recvMessage()
            print(ss)
    def end(self):
        self.sock.close()

class myGUI:
    def __init__(self):
        self.root = Tk()

        self.row = 4
        self.column = 4
        self.size = 100
        self.field = [[0 for j in range(self.column)] for i in range(self.row)]
        self.block = 3
        self.drink = 4
        self.drinkpos = []
        self.curx = 0
        self.cury = 0

        self.curdir = 0

        # self.bluetooth = BlueTooth()
        self.father = [[[-1, -1] for j in range(self.column)] for i in range(self.row)]
        self.drinkpos = []

        self.dx = [0, 1, 0, -1]
        self.dy = [1, 0, -1, 0]

        self.bt = BlueTooth()


    def paintCanvas(self):
        cnt = 1
        for i in range(0, self.row):
            for j in range(0, self.column):
                if (i==self.curx and j == self.cury):
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "green")
                    self.LeftCanvas.create_text([self.size*(i+0.5), self.size*(j+0.5)], text = 'direction = ' + str([self.dx[self.curdir], self.dy[self.curdir]]), fill = "white")
                    continue
                if (self.field[i][j] == -1):
                    print("i, j " + str(i) + " " + str(j))
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "red")
                elif (self.field[i][j] == -2):
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "black")
                    self.LeftCanvas.create_text([self.size*(i+0.5), self.size*(j+0.5)], text = 'survivor', fill = "white")
                    # cnt = cnt + 1
                else:
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "black")
        for i in range(0, self.row):
            self.LeftCanvas.create_line([0, i*self.size, self.column*self.size, i*self.size], fill = "white")
        for i in range(0, self.column):
            self.LeftCanvas.create_line([i*self.size, 0, i*self.size, self.column*self.size], fill = "white")

        for i in range(0, self.column):
            self.LeftCanvas.create_text([self.size*(i+0.5), self.size*self.column+25], text = str(i),fill = "black")
        for i in range(0, self.row):
            self.LeftCanvas.create_text([self.size*self.row + 25, self.size*(i+0.5)], text = str(i),fill = "black")

        self.LeftCanvas.create_text([15, self.size*self.column+25], text = "x", fill = "black")
        self.LeftCanvas.create_text([self.size*self.row+25, 10], text = "y",fill = "black")
        self.root.update()

    def updateField(self):
        self.field = [[0 for j in range(self.column)] for i in range(self.row)]
        print(self.numberofBK.get())
        print(self.numberofDK.get())
        self.block = int(self.numberofBK.get())
        self.drink = int(self.numberofDK.get())
        self.curx = 0
        self.cury = 0
        self.curdir = 0
        for i in range(0, self.block):
            x = 0
            y = 0
            while ((x == 0 and y == 0) or (self.field[x][y] == -1)):
                x = random.randint(0, self.row-1)
                y = random.randint(0, self.column-1)
            self.field[x][y] = -1
            print("x, y " + str(x) + " " + str(y))

        for i in range(0, self.drink):
            x = 0
            y = 0
            while ((x == 0 and y == 0) or (self.field[x][y] == -1) or (self.field[x][y] == -2)):
                x = random.randint(0, self.row-1)
                y = random.randint(0, self.column-1)
            self.field[x][y] = -2
            print("x, y " + str(x) + " " + str(y))
        self.paintCanvas()

    def updateMap(self):
        self.updateField()

    def inrange(self, x, y):
        return 0 <= x and x < self.row and 0<= y and y < self.column
    def BFS(self):
        que = queue.Queue()
        self.vis = [[-1 for j in range(self.column)] for i in range(self.row)]
        x = 0
        y = 0
        que.put([x, y])
        self.vis[x][y] = 1
        while (que.empty() == False):
            cur = que.get()
            x = cur[0]
            y = cur[1]
            if (self.field[x][y] == -2):
                self.drinkpos.append([x, y])
            for i in range(len(self.dx)):
                nx = x + self.dx[i]
                ny = y + self.dy[i]
                print("nx ny " + str(nx) + " " + str(ny))
                if (self.inrange(nx, ny) and self.vis[nx][ny] == -1 and self.field[nx][ny] != -1):
                    que.put([nx, ny])
                    self.vis[nx][ny] = self.vis[x][y] + 1
                    self.father[nx][ny] = [x, y]

        for j in range(0, self.column):
            for i in range(0, self.row):
                print(self.father[i][j], end = ' ')
            print('')
        for j in range(0, self.column):
            for i in range(0, self.row):
                print(self.vis[i][j], end = ' ')
            print('')


    def getPath(self, pos):
        ret = []

        print("in getPath pos = " + str(pos))
        while (not(pos[0] == -1 and pos[1] == -1)):
            ret.append(pos)
            pos = self.father[pos[0]][pos[1]]
        ret = list(reversed(ret))
        print("ret = " + str(ret))
        return ret

    def cross_product(self, host, guest):
        return host[0]*guest[1] - guest[0]*host[1]
    def go_back(self, path):
        print("in go path = " + str(path))
        self.bt.sendMessage('o')
        while (str(self.bt.recvMessage()) != "ok"):
            continue
        for i in range(1, len(path)):
            aim_dir = [path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]]
            cur_dir = [self.dx[self.curdir], self.dy[self.curdir]]

            print("current dir = " + str([self.dx[self.curdir], self.dy[self.curdir]]))
            if (self.cross_product(cur_dir, aim_dir) < 0):
                self.curdir = (self.curdir+1+4)%4;
                self.bt.sendMessage('l')
                self.paintCanvas()
                while (str(self.bt.recvMessage()) != "ok"):
                    continue
            elif (self.cross_product(cur_dir, aim_dir) > 0):
                self.curdir = (self.curdir-1+4)%4;
                self.bt.sendMessage('r')
                self.paintCanvas()
                while (str(self.bt.recvMessage()) != "ok"):
                    continue
            print("current pos = " + str([self.curx, self.cury]))
            print("current dir = " + str([self.dx[self.curdir], self.dy[self.curdir]]))

            self.curx = self.curx + self.dx[self.curdir]
            self.cury = self.cury + self.dy[self.curdir]
            self.bt.sendMessage('f')
            self.paintCanvas()
            while (str(self.bt.recvMessage()) != "ok"):
                continue
        self.bt.sendMessage('c')
        while (str(self.bt.recvMessage()) != "ok"):
            continue
        self.curdir = (self.curdir+2)%4
        self.bt.sendMessage('b')
        self.paintCanvas()
        while (str(self.bt.recvMessage()) != "ok"):
            continue

        path = list(reversed(path))
        for i in range(1, len(path)):
            aim_dir = [path[i][0] - path[i-1][0], path[i][1] - path[i-1][1]]
            cur_dir = [self.dx[self.curdir], self.dy[self.curdir]]

            print("current dir = " + str([self.dx[self.curdir], self.dy[self.curdir]]))
            if (self.cross_product(cur_dir, aim_dir) < 0):
                self.curdir = (self.curdir+1+4)%4;
                self.bt.sendMessage('l')
                self.paintCanvas()
                while (str(self.bt.recvMessage()) != "ok"):
                    continue
            elif (self.cross_product(cur_dir, aim_dir) > 0):
                self.curdir = (self.curdir-1+4)%4;
                self.bt.sendMessage('r')
                self.paintCanvas()
                while (str(self.bt.recvMessage()) != "ok"):
                    continue
            print("current pos = " + str([self.curx, self.cury]))
            print("current dir = " + str([self.dx[self.curdir], self.dy[self.curdir]]))

            self.curx = self.curx + self.dx[self.curdir]
            self.cury = self.cury + self.dy[self.curdir]
            self.bt.sendMessage('f')
            self.paintCanvas()
            while (str(self.bt.recvMessage()) != "ok"):
                continue
        self.bt.sendMessage('o')
        while (str(self.bt.recvMessage()) != "ok"):
            continue
        self.curdir = (self.curdir+2)%4
        self.bt.sendMessage('b')
        self.paintCanvas()
        while (str(self.bt.recvMessage()) != "ok"):
            continue
        time.sleep(0.2)
    def getDrink(self):
        self.drinkpos = []
        self.BFS()
        for pos in self.drinkpos:
            path = self.getPath(pos)
            self.go_back(path)
           # break;

    def run(self):
        self.root.title("Sparki")
        self.root.geometry("700x450")

        self.left = Frame(self.root, height = 450, width = 450,bg = "black")
        self.left.pack(side = "left")

        self.right = Frame(self.root, height = 400, width = 200,bg = "red")
        self.right.pack(side = "top")


        # the map build part
        self.blockLabel = Label(self.right, text="number of fire blocks:")
        self.blockLabel.grid(row = 1, column = 1)
        self.numberofBK = Entry(self.right)
        self.numberofBK.insert(0, str(3))
        self.numberofBK.grid(row = 1, column = 2)

        self.blockLabel = Label(self.right, text="number of surviors:")
        self.blockLabel.grid(row = 2, column = 1)
        self.numberofDK = Entry(self.right)
        self.numberofDK.insert(0, str(4))
        self.numberofDK.grid(row = 2, column = 2)

        self.updateMap = Button(self.right, text="UpdateMap", command = self.updateMap)
        self.updateMap.grid(row = 3, column = 2)

        self.getDrink = Button(self.right, text="rescue all surviors", command = self.getDrink)
        self.getDrink.grid(row = 4, column = 1)

        self.blockLabel = Label(self.right, text="number of surviors:")
        self.blockLabel.grid(row = 2, column = 1)

        self.LeftCanvas = Canvas(self.left, width=450, height=450)
        self.updateField()
        self.LeftCanvas.pack(side = "left")


        self.root.mainloop()


if __name__ == '__main__':
    gui = myGUI()
    gui.run()
