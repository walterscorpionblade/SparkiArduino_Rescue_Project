import bluetooth

#This is just a test file to test if we can use laptop to cummunicate with sparki!
class BlueTooth:
    def __init__(self, addr = "98:D3:31:FC:46:BF"):
        self.bd_addr = addr
        self.port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((bd_addr, self.port))
    # We specified that every message is ended with a '#'

    def sendMessage(self, string):
        print("send " + str(string))
        self.sock.send(string)
        self.sock.send('#')

    def recvMessage(self):
        # I don't know why, but I have to write at this way to make it right
        ret = ''
        ss = self.sock.recv(1000)
        for ch in ss:
            ret = ret + str(chr(ch))
        while (ret[-1] != '#'):
            ss = self.sock.recv(1000)
            for ch in ss:
                ret = ret + str(chr(ch))
        return ret[0:-1]

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

bd_addr = "98:D3:31:FC:46:BF"
bt = BlueTooth(bd_addr)
bt.test()
# bd_addr = input("input the address")
