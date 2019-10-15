#以不同的颜色区别各个frame

from tkinter import *

class myGUI:
    def __init__(self):
        self.root = Tk()

        self.root.title("Sparki")
        self.root.geometry("610x400")

        
        self.left = Frame(self.root, height = 400,width = 400,bg = "yellow")
        self.left.pack(side = "left")
        
        self.right = Frame(self.root, height = 400,width = 200,bg = "white")
        self.right.pack(side = "right")
        
        self.mid = Frame(self.root, height = 400,width = 10,bg = "black")
        self.mid.pack(side = "left")
        
        self.points = []
        self.LeftCanvas = Canvas(self.left, width=400, height=400)
        self.LeftCanvas.create_oval([199, 199, 201, 201])
        self.points.append([200, 200])

        self.LeftCanvas.bind(sequence="<Motion>", func=self.processMouseMotion)
        self.LeftCanvas.bind(sequence="<Double-Button-1>", func=self.processMouseDoubleClick)

        self.LeftCanvas.pack(side = "left")
        
         

        
        self.messageLevel= Frame(self.right, height = 200, width = 20, bg = "red")
        self.messageLevel.pack(side = "top")
        
        self.InputLevel = Frame(self.right, height = 200, width = 20, bg = "red")
        self.InputLevel.pack(side = "top")
        
        self.buttonLevel= Frame(self.right, height = 200, width = 20, bg = "red")
        self.buttonLevel.pack(side = "top")
        
    
        self.confirm = Button(self.buttonLevel, text="confirm", command=self.confirmcallback)
        self.confirm.pack(side = "left")
        
        self.clear = Button(self.buttonLevel, text="clear", command=self.clearcallback)
        self.clear.pack(side = "right")
        
        self.xmsg = Message(self.messageLevel, width = 100, text="X_coordinate")
        self.xmsg.pack(side = "left")
        
        self.ymsg = Message(self.messageLevel, width = 100, text="Y_coordinate")
        self.ymsg.pack(side = "right")
        
        self.x1 = Entry(self.InputLevel, width = 16)
        self.x1.pack(side = "left")
        
        self.y1 = Entry(self.InputLevel, width = 16)
        self.y1.pack(side = "right")
    def run(self):
        self.root.mainloop()
    def clearcallback(self, event):
        self.LeftCanvas.delete(ALL)
        self.LeftCanvas.create_oval([199, 199, 201, 201])
        self.points.append([200, 200])
        self.LeftCanvas.pack()
    
    def confirmcallback(self, event):
        self.LeftCanvas.delete(ALL)
        self.LeftCanvas.create_oval([199, 199, 201, 201])
        self.points = []
        self.points.append([200, 200])
        self.LeftCanvas.pack()
    
    
    
    def processMouseMotion(self, event):
        self.x1.delete(0, END)
        self.y1.delete(0, END)
        self.x1.insert(0, str(event.x))
        self.y1.insert(0, str(event.y))
        self.x1.pack()
        self.y1.pack()
    
        # print("位于窗口", me.x, me.y)
        # print("位于窗口", me.num)
    
    def processMouseDoubleClick(self, event):
        self.points.append([event.x, event.y])
        self.LeftCanvas.create_oval([event.x-1, event.y-1, event.x+1, event.y+1])
    
        self.LeftCanvas.create_line([self.points[-2][0], self.points[-2][1], event.x, event.y])

if __name__ == '__main__':
    gui = myGUI()
    gui.run()


