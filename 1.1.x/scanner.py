from tkinter import *
import socket

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Insira um IP para um Host ou um range de IPs para uma Rede:')
        self.lbl4=Label(win, text='Exemplo de Rede: 192.168.1.3-192.168.1.90')
        self.lbl2=Label(win, text='Insira um Range de portas (Exemplo 1-100):')
        self.lbl3=Label(win, text='Selecione o Protocolo (Uma opcao por Scan):')
        self.t1=Entry(bd=3)
        self.t2=Entry(bd=3)
        self.var1 = IntVar()
        self.y = Checkbutton(win, text="TCP", variable=self.var1)
        self.var2 = IntVar()
        self.x = Checkbutton(win, text="UDP", variable=self.var2)
        self.btn1 = Button(win, text='Scan')
        self.lbl1.place(x=50, y=50)
        self.t1.place(x=100, y=100)
        self.lbl2.place(x=50, y=150)
        self.lbl4.place(x=50, y=70)
        self.t2.place(x=100, y=200)
        self.b1=Button(win, text='Scan', command=self.run)
        self.b1.place(x=400, y=400)
        self.x.place(x=70, y=350)
        self.y.place(x=70, y=400)
        self.lbl3.place(x=50, y=300)
        self.dic_port = {}
        self.list = []

    def scan(self, port, target):
        if self.var1.get() == 1: 
            print("Escaneando Porta", port)
            sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            socket.setdefaulttimeout(1)
            try:
                sockt.connect((target, port))
                serv = socket.getservbyport(port, "tcp")
                print('[*] Porta', port, '/tcp','ta aberta')
                print(str(serv))
                self.list.append('[*] Porta '+ str(port)+ ' /TCP'+' ta aberta' + ' rodando o Servico: ' + str(serv))
                sockt.close()
            except Exception as e:
                sockt.close()
                print(e)
        elif self.var2.get() == 1:
            print("Escaneando Porta", port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.connect((target, port))
                serv = socket.getservbyport(port, "udp")
                print('[*] Porta', port, '/udp','ta aberta')
                print(str(serv))
                self.list.append('[*] Porta '+ str(port)+ ' /UDP'+' ta aberta' + ' rodando o Servico: ' + str(serv))
                sock.close()
            except Exception as e:
                sock.close()
                print(e)
    
    def run(self):
        ip_range = self.t1.get().split('-')
        ips = ip_range[0].split('.')
        if len(ip_range) == 1:
            ip_range.append(ip_range[0])            
        ip_ultimo = ip_range[1].split('.')[3]
        string = ips[0] + ips[1] 
        portas = self.t2.get().split('-')
        for i in range(int(ips[3]), int(ip_ultimo) + 1): 
            target = ips[0] +'.'+ ips[1] +'.'+ ips[2] +'.'+ str(i)
            self.list = []
            print(self.list)
            for j in range(int(portas[0]), int(portas[1]) + 1):
                self.scan(j, target)
            self.dic_port[target] = self.list
            print(self.dic_port)
        
        result = Tk()
        scrollbar = Scrollbar(result)
        scrollbar.pack(side=RIGHT, fill=Y)
        txt = Listbox(result)
        txt.pack(fill=BOTH, expand=1)
        result.geometry("500x700+10+10")
        result.title('RESULT')
        for i in self.dic_port:
            if len(self.dic_port[i]) != 0:
                txt.insert(END, '\n'+i+':')
                for j in self.dic_port[i]:
                    txt.insert(END, j)

        txt.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=txt.yview)



window=Tk()
mywin=MyWindow(window)
window.title('Port Scanner')
window.geometry("600x500+10+10")
window.mainloop()