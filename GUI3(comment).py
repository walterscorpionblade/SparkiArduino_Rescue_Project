#以不同的颜色区别各个frame

from tkinter import *
# 这里的 tkinter 就是 GUI 用的图形库，为了简单，使用 python 自带的图形库
import random
import time
import bluetooth

import queue

class BlueTooth:
    def __init__(self, addr = "98:D3:31:FC:46:BF"):
        # 上面是sparki的地址，由于只有一台机器，所以干脆写成默认值
        self.bd_addr = addr
        self.port = 1
        # 指定端口
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        # 指定连接模式
        self.sock.connect((self.bd_addr, self.port))
        # 发起连接，如果没有报错就是连接成功
    # We specified that every message is ended with a '#'

    def sendMessage(self, string):
        print("send " + str(string))
        # 上面这个print 打印调试信息
        self.sock.send(string)
        # 调用sock 的接口 发送字符串
        self.sock.send('#')
        # 我们约定好 以 # 作为一段命令的终止符号，这里发送终止符

    def recvMessage(self):
        # I don't know why, but I have to write at this way to make it right
        ret = ''
        ss = self.sock.recv(1000)
        # 从端口处接收最多1000个字符，因为命令很短，所以1000绰绰有余
        for ch in ss:
            ret = ret + str(chr(ch))
        while (ret[-1] != '#'):
            ss = self.sock.recv(1000)
            for ch in ss:
                ret = ret + str(chr(ch))
        # 上面一段循环判断接收到的字符串最后一个字符是否是 # 终止符
        print("revc = " + str(ret))
        # 上面这个print 打印调试信息，看看而已啦
        return str(ret[0:-1])
        # 之所以0:-1 是因为最后一个字符是终止符，不需要返回

    def test(self):
        while True:
            data = input()
            if len(data) == 0:
                break
            self.sendMessage(str(data))
            ss = self.recvMessage()
            print(ss)
    # 上面这一段用于测试，就是发送消息，然后看spriki 能不能准确收到而已
    def end(self):
        self.sock.close()
    # 切断连接的命令

class myGUI:

    def __init__(self):
        self.root = Tk()
        # 这里使用的是python 自带的GUI 框架，这里是建立一个实例

        self.row = 4
        self.column = 4
        # row 和 column 是指行和列 根据要求，是4*4
        self.size = 100
        # 这里的 size 是指 每个格子 的边长
        self.field = [[0 for j in range(self.column)] for i in range(self.row)]
        # 这里的 fielf 用于建立，那个格子的地图， i行，j列
        self.block = 3
        self.drink = 4
        # block 是指障碍物的个数， drink 是饮料的个数，这里预先设定为3， 和4，之后可以在程序界面中直接设置，不建议设置太多block 图会不连通

        self.drinkpos = []
        # drinkpos 用来记录 饮料的坐标
        self.curx = 0
        self.cury = 0
        # curx,cury 记录小车当前的位置


        self.curdir = 0 
        # curdir 记录小车当前的方向

        self.father = [[[-1, -1] for j in range(self.column)] for i in range(self.row)]
        # 我们稍后会使用 bfs 算法去寻找小车到每个地图上的位置的最短路，这里的father 记录的是每个节点由哪个节点而来，我们只要顺着节点的父亲一直走，就可以回到出发点

        self.dx = [0, 1, 0, -1]
        self.dy = [1, 0, -1, 0]
        # 这里的dx, dy 盗用为微积分中的微分符号， 一个节点在地图上能往四个方向走分别是[dx[i], dy[i]]， i 可以取0,1,2,3

        self.bt = BlueTooth()
        # 这里建立一个蓝牙连接


    def paintCanvas(self):
        cnt = 1
        for i in range(0, self.row):
            for j in range(0, self.column):
                if (i==self.curx and j == self.cury):
                    # 如果这个点是当前小车所在的点，我们画一个绿的的正方形，同时用文字标出方向
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "green")
                    self.LeftCanvas.create_text([self.size*(i+0.5), self.size*(j+0.5)], text = 'direction = ' + str([self.dx[self.curdir], self.dy[self.curdir]]), fill = "white")
                    continue
                if (self.field[i][j] == -1):
                    # 如果这个点是障碍物，我们画一个红色的正方形
                    print("i, j " + str(i) + " " + str(j))
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "red")
                elif (self.field[i][j] == -2):
                    # 如果这个点是饮料，我们话黑色正方形，并写上白色文字用于标明
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "black")
                    self.LeftCanvas.create_text([self.size*(i+0.5), self.size*(j+0.5)], text = 'drink', fill = "white")
                    # cnt = cnt + 1
                else:
                    # 如果这个点是正常的可以行走的点，我们单纯画一个黑色的格子
                    self.LeftCanvas.create_rectangle([self.size*i, self.size*j, self.size*(i+1), self.size*(j+1)], fill = "black")

        # ***********************以下代码用于绘制图中的白线，将格子一个个抠出来
        for i in range(0, self.row):
            self.LeftCanvas.create_line([0, i*self.size, self.column*self.size, i*self.size], fill = "white")
        for i in range(0, self.column):
            self.LeftCanvas.create_line([i*self.size, 0, i*self.size, self.column*self.size], fill = "white")

        for i in range(0, self.column):
            self.LeftCanvas.create_text([self.size*(i+0.5), self.size*self.column+25], text = str(i),fill = "black")
        for i in range(0, self.row):
            self.LeftCanvas.create_text([self.size*self.row + 25, self.size*(i+0.5)], text = str(i),fill = "black")
        # ***********************以上代码用于绘制图中的白线，将格子一个个抠出来

        # ***********************以下代码用于标明坐标，就是写一个x,一个y
        self.LeftCanvas.create_text([15, self.size*self.column+25], text = "x", fill = "black")
        self.LeftCanvas.create_text([self.size*self.row+25, 10], text = "y",fill = "black")
        self.root.update()
        # ***********************以上代码用于标明坐标

    def updateField(self):
        self.field = [[0 for j in range(self.column)] for i in range(self.row)]
        print(self.numberofBK.get())
        print(self.numberofDK.get())
        self.block = int(self.numberofBK.get())
        self.drink = int(self.numberofDK.get())
        # 从饮料和方块的输入框中 获取数据

        self.curx = 0
        self.cury = 0
        self.curdir = 0
        # 初始化小车所在位置

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
        # 这里的两个for循环是是使用随机处理产生饮料和障碍物所在的坐标

        self.paintCanvas()
        # paintCanvas 这个函数用于绘制图形

    def updateMap(self):
        self.updateField()
        # 更新地图，按下update 按钮会执行这个程序

    def inrange(self, x, y):
        # 这个in range 用于判断一个坐标是否还在地图内，和下面的BFS配合使用
        return 0 <= x and x < self.row and 0<= y and y < self.column
    def BFS(self):
        que = queue.Queue()
        # 如果要使用广度优先搜索，所以先定义一个队列

        self.vis = [[-1 for j in range(self.column)] for i in range(self.row)]
        # vis 意为 visted -1代表没有被访问过

        x = 0
        y = 0
        que.put([x, y])
        self.vis[x][y] = 1
        while (que.empty() == False):
            # 当队列非空的时候，搜索可以一直执行下去

            cur = que.get() 
            x = cur[0]
            y = cur[1]
            if (self.field[x][y] == -2):
                self.drinkpos.append([x, y])
            for i in range(len(self.dx)):
                # 这里的 for 循环实际上是遍历当前位置可以行走的4个方向
                nx = x + self.dx[i]
                ny = y + self.dy[i]
                # nx: new_x
                # ny: new_y
                # 当前的坐标x, y加上方向，产生新的坐标

                print("nx ny " + str(nx) + " " + str(ny))

                if (self.inrange(nx, ny) and self.vis[nx][ny] == -1 and self.field[nx][ny] != -1):
                    # 这里if语句的意思是说，如果这个新的坐标是在地图内的，而且，没有被访问过的，而且，并不是一个障碍物的
                    # 那么我们就
                    
                    que.put([nx, ny])
                    # 将这个新的坐标添加到队列中
                    
                    self.vis[nx][ny] = self.vis[x][y] + 1
                    # 记录nx,ny这个位置已经走过了，实际上，vis记录了从出发到当这个位置的距离，我从x, y来，那么x，y的距离加上1就是我的距离
                    self.father[nx][ny] = [x, y]
                    # 记录这个新节点的父亲是哪个坐标
                    
        # 下面两个for 循环用于测试，可以删掉，他们只是打印每个节点的父亲，和每个节点到出发点的距离
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
        # 代码并不复杂，由于图中的路径是用 father 来记录的，所以，我们沿着father 一路走上去，然后将路径倒过来就可以了
        return ret

    # def listequal(self, lst1, lst2):
        # if (len(lst1) == len(lst2)):
            # for i in range(lst1):
                # if (lst1[i] != lst2[i]):
                    # return False
            # return True
        # return False
    def cross_product(self, host, guest):
        return host[0]*guest[1] - guest[0]*host[1]
        # 点积，host和guest是两个二维向量 
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
    def getDrink(self):
        self.drinkpos = []
        self.BFS()
        # 执行BFS 从起始点出发访问每个点
        for pos in self.drinkpos:
            path = self.getPath(pos)
            # 获取有起始点到每个点的路径
            self.go_back(path)
            # 执行命令，使方块由起始点出发到达目的地，然后再走回去

    def run(self):
        self.root.title("Sparki")
        # 这里说明这个窗口程序的标题是 sparki
        self.root.geometry("700x450")
        # 设置这个窗口的大小
        
        self.left = Frame(self.root, height = 450, width = 450,bg = "black")
        self.left.pack(side = "left")
        
        self.right = Frame(self.root, height = 400, width = 200,bg = "red")
        self.right.pack(side = "top")

        # 整个窗口分为left 和 right 两部分，Frame中的选项分别是（依附于那个图形元件，高度，宽度，颜色）


        # the map build part
        self.blockLabel = Label(self.right, text="number of blocks:")
        self.blockLabel.grid(row = 1, column = 1)
        self.numberofBK = Entry(self.right)
        self.numberofBK.insert(0, str(3))
        self.numberofBK.grid(row = 1, column = 2)
        # Label 是一段文字描述
        # Entry 是一个输入窗口
        # grid 是一个用于设置位置的东西，可以把他想象成一个矩阵，row 和 column 是相应的坐标

        self.blockLabel = Label(self.right, text="number of drinks:")
        self.blockLabel.grid(row = 2, column = 1)
        self.numberofDK = Entry(self.right)
        self.numberofDK.insert(0, str(4))
        self.numberofDK.grid(row = 2, column = 2)
        # 与上同，这里是设置饮料个数的输入窗口

        self.updateMap = Button(self.right, text="UpdateMap", command = self.updateMap)
        self.updateMap.grid(row = 3, column = 2)
        # 设置 Button 如果按下 UPdate 会调用self.updateMap 函数

        self.getDrink = Button(self.right, text="getAllDrink", command = self.getDrink)
        self.getDrink.grid(row = 4, column = 1)
        # 这里是一个启动按钮，按下去以后,调用self.getDrink函数

        self.blockLabel = Label(self.right, text="number of drinks:")
        self.blockLabel.grid(row = 2, column = 1)

        self.LeftCanvas = Canvas(self.left, width=450, height=450)
        self.updateField()
        self.LeftCanvas.pack(side = "left")
        # 这里是左边的Canvas 图形元件，可以绘图

        self.root.mainloop()
        # 这行命令用于启动图形界面


if __name__ == '__main__':
    gui = myGUI()
    gui.run()


