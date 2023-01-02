import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import *
import threading
import time
import sys
loaded = False
username = None
previos = 0
amogus = []
stop_threads = False
#loading_room
def loadlogin_page():
    global server
    try:
        global cursor
        global conn
        conn = psycopg2.connect(database="b3kduxnyvomepxd8txkb",host="b3kduxnyvomepxd8txkb-postgresql.services.clever-cloud.com",user="u29a8cs8uwb6bw0dtgnr",password="T489iWAf87DXMyWhabW5",port="5432")
        cursor = conn.cursor()
        loaded = True
        root.destroy()
    except:
        label = tk.Label(root, text="                                                          ")
        label.pack()
        label.place(relx=0.5, rely=0.5, anchor="center")
        label = tk.Label(root, text="Failed")
        label.pack()
        label.place(relx=0.5, rely=0.5, anchor="center")
    
root = tk.Tk()
root.title("Namo's Chat Client")
root.geometry('425x250')
label = tk.Label(root, text="Connecting to server...")
label.pack()
label.place(relx=0.5, rely=0.5, anchor="center")

root.after(200, loadlogin_page)
root.mainloop()
#login_room
root = tk.Tk()
root.title("Namo's Chat login")
root.geometry('825x450')
def login(event=None):
    global username
    inp = inputtxt.get(1.0, "end-1c")
    inputtxt.delete('1.0', END)
    print(inp)
    if inp == '':
        return
    username = inp
    try:
        #soon:tm:
        #fileexist = server.stat(f'/home/namo/discock/user/{inp}.txt')
        root.destroy()
    except IOError:
        #soon:tm:
        #server.open(f'/home/namo/discock/user/{inp}.txt', 'x')
        usercrea = tk.Label(root,text = "User Created!")
        usercrea.pack()
inputtxt = tk.Text(root,height = 2,width = 30)
inputtxt.pack()
inputtxt.place(relx=0.5, rely=0.5, anchor="center")
printButton = tk.Button(root,text = "Login",command = login, height = 2)
printButton.pack(side=RIGHT)
printButton.place(relx=0.7, rely=0.5, anchor="center")
print(f'auth: {loaded}')
root.bind('<Return>', login)
root.mainloop()
#chat_room

root = tk.Tk()

def reconnect():
    print('reconnectig')
    if stop_threads:
        return
    global cursor
    global conn
    try:
        conn = psycopg2.connect(database="b3kduxnyvomepxd8txkb",host="b3kduxnyvomepxd8txkb-postgresql.services.clever-cloud.com",user="u29a8cs8uwb6bw0dtgnr",password="T489iWAf87DXMyWhabW5",port="5432")
        cursor = conn.cursor()
    except:
        pass
    reconnecttext.destroy()

def updatechat():
    while True:
        global row
        time.sleep(0.5)
        if stop_threads:
            break
        global previos
        global reconnecttext
        cursor.execute("SELECT * FROM sustable")
        try:
            rows = cursor.fetchall()
        except:
            reconnecttext = tk.Label(root, text="Reconnecting...")
            reconnecttext.pack()
            reconnecttext.place(relx=0.5, rely=0.5, anchor="center")
            threading.Thread(target=reconnect).start()
            pass
        try:
            if rows == previos:
                pass
            else:
                tree.delete(*tree.get_children())
                for row in rows:
                    tree.insert("", tk.END, values=row)
                tree.yview_moveto(1)
            previos = rows
        except:
            pass

def sendchat(event=None):
    if stop_threads:
        return
    inp = inputtxt.get(1.0, "end-1c")
    inputtxt.delete('1.0', END)
    if inp == '':
        return
    cursor.execute("INSERT INTO sustable (item1,item2) VALUES (%s,%s) returning sustable",(username,inp))
    conn.commit()
    sendingtext.destroy()

def sendchat_load(event=None):
    if stop_threads:
        return
    global sendingtext
    sendingtext = tk.Label(root, text="Sending...")
    sendingtext.pack()
    sendingtext.place(relx=0.5, rely=0.5, anchor="center")
    threading.Thread(target=sendchat).start()

if username == None:
    root.destroy()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
root.title("Namo's Chat")
root.geometry('825x450')
tree = ttk.Treeview(root, column=("c1", "c2"), show="tree")
tree['show'] = 'headings'
tree.column("#0", width=0)
tree.column("#1", minwidth=0, width=100, stretch=NO)
tree.heading("#1", text="Name")
tree.column("#2")
tree.heading("#2", text="Message")
tree.pack(fill="both", expand=True)
inputtxt = tk.Text(root,height = 3,width = 90)
inputtxt.pack(anchor = "s", side = "left")
printButton = tk.Button(root,text = "Send",command = sendchat_load, height = 3, width=10)
printButton.pack(anchor = "s", side = "right")
root.bind('<Return>', sendchat_load)
root.after(100, (threading.Thread(target=updatechat).start))
def on_closing():
   global stop_threads
   top= Toplevel(root)
   top.geometry("425x250")
   top.title("Closing")
   label = tk.Label(root, text="Closing connection...")
   label.pack()
   label.place(relx=0.5, rely=0.5, anchor="center")
   conn.close()
   label.destroy()
   stop_threads = True
   label = tk.Label(root, text="Stoping thread...")
   label.pack()
   label.place(relx=0.5, rely=0.5, anchor="center")
   label.destroy()
   root.destroy()
   sys.exit()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()