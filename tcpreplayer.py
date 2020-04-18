import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import netifaces
import os
from subprocess import check_output
def get_pid(name):
    return check_output(["pidof",name])

def startFunction():
    print("You clicked start Button")
    try:
        if(loopSending.get() !=0):
            command = "tcpreplay --pid -i " + listBox.get(listBox.curselection())  + " --loop " + loopNumber.get() + " " + m.filename + " &"
        else:
            command = "tcpreplay --pid -i " + listBox.get(listBox.curselection())+ " " + m.filename + " &"
        print(command)
        os.system(command)
        
        
    except:
        response = messagebox.showwarning("WARNING", "Please select an adapter!!")


def stopFunction():
    print("You clicked stop Button")
    print(get_pid("tcpreplay"))
    pid = ''.join(chr(i) for i in get_pid("tcpreplay"))
    command = "kill -9 " + pid
    os.system(command)  

def getInterfaceNames():
    return netifaces.interfaces()

def insertInterfaces():
    interfaceList = getInterfaceNames()
    lenInterfaceList = len(interfaceList)
    for i in range(lenInterfaceList):
        listBox.insert(i,interfaceList[i])
    return interfaceList

def findIpAddresses():
    print(listBox.get(listBox.curselection()))
    
    try:
        ipaddress = netifaces.ifaddresses(listBox.get(listBox.curselection()))[2][0]['addr']
        netmask = netifaces.ifaddresses(listBox.get(listBox.curselection()))[2][0]['netmask']
        printMsg = f"{ipaddress} {netmask}"
        print(printMsg)
        messagebox.showinfo("Network settings", printMsg)
    except:
        print("KABLOYU BAGLA.")
        response = messagebox.showwarning("WARNING", "Please open the board\n or connect the cable!!!\nAre you ready?")
        if response:
            findIpAddresses()

def lol():
    clicked_items = listBox.get(listBox.curselection())
    print(clicked_items)
    for item in clicked_items:
        print(listBox.get(item))

m = tk.Tk() 
m.title('NTK TCP Replayer')
button = tk.Button(m, text='Start', width=25, command=startFunction)
button.pack()
button = tk.Button(m, text='Stop', width=25, command=stopFunction)
button.pack()
button = tk.Button(m, text='Close', width=25, command=m.destroy)
button.pack()
loopSending = tk.IntVar()
loopChecker = tk.Checkbutton(m,text='Loop Sending',variable=loopSending)
loopChecker.pack()
loopNumber = tk.Entry(m)
loopNumber.pack()
listBox = tk.Listbox(m,selectmode=SINGLE)
listBox.activate(0)
listBox.pack()
interfaceListReturn = insertInterfaces()
m.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pcap files","*.pcap"),("all files","*.*")))




showButton = tk.Button(m, text='Show IP address', width=25, command=findIpAddresses)
showButton.pack()









m.mainloop()
