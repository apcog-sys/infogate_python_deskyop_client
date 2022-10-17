import tkinter as tk
from tkinter import Listbox, messagebox
from tkinter import filedialog
from tkinter import *
import json
from tkinter import ttk
from urllib import response
import webbrowser
import requests
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="infogate_python"
)

mycursor = mydb.cursor()
my_list = [];

form = tk.Tk()
form.title("Infogate client")
form.geometry("500x280")

tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text="Registration")
tab_parent.add(tab2, text="Rooms")
tab_parent.add(tab3, text="messages")
tab_parent.add(tab4, text="room keys")

# === WIDGETS FOR TAB ONE
def open_login():
        print('username --> ', usernameEntryTabOne.get())
        print('password--> ', pwdEntryTabOne.get())

        data = {
            "user_name": usernameEntryTabOne.get(),
            "password": pwdEntryTabOne.get(),
        }
        url = "http://localhost:3000/user/login"
        r = requests.post(url=url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }, json={
            "user_name": usernameEntryTabOne.get(),
            "password": pwdEntryTabOne.get(),
        })
        print("JSON Response ", r.json())
        response = r.json()
        try:
            if(response['token']):
                    print(response['result']['id'])
                    print(response['token'])
                    sql = "INSERT INTO user_registration (id,user_name,password,account_key,entity_name,role_name,contact_details,person_or_app_name,role_ids,pub_rooms,sub_rooms,status,token) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)"
                    val = (str(response['result']['id']),
                        str(response['result']['user_name']),
                        str(response['result']['password']),
                        str(response['result']['account_key']),
                        str(response['result']['entity_name']),
                        str(response['result']['role_name']),
                        str(response['result']['contact_details']),
                        str(response['result']['person_or_app_name']),
                        str(response['result']['role_ids']),
                        str(response['result']['pub_rooms']),
                        str(response['result']['sub_rooms']),
                        str(response['result']['status']),
                        str(response['token']),
                        )
                    print(val)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
                    messagebox.showinfo('logged in')
        except:
            messagebox.showinfo(response['Ack'])
  


def open_registration():
    webbrowser.open('http://localhost:3000/registration')


usernameLabelTabOne = tk.Label(tab1, text="User Name")
pwdLabelTabOne = tk.Label(tab1, text="password")

usernameEntryTabOne = tk.Entry(tab1)
pwdEntryTabOne = tk.Entry(tab1)

buttonForward = tk.Button(tab1, text="Register", command=open_registration)
buttonBack = tk.Button(tab1, text="Login", command=open_login)

# === ADD WIDGETS TO GRID ON TAB ONE
usernameLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
usernameEntryTabOne.grid(row=0, column=1, padx=15, pady=15)

pwdLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
pwdEntryTabOne.grid(row=1, column=1, padx=15, pady=15)
buttonBack.grid(row=3, column=0, padx=15, pady=15)

buttonForward.grid(row=3, column=2, padx=15, pady=15)


# === WIDGETS FOR TAB TWO
def gettoken():
    mycursor.execute("SELECT token FROM user_registration")
    myresult = mycursor.fetchone()
    for x in myresult:
        return x


def getroomlist():
    print('token --> ', token_val)
    global listbox
    url = "http://localhost:3000/room/get"

    r = requests.post(url=url, headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token_val,
    })
    print("JSON Response ", r.json())
    global my_list
    for each in r.json():
        print(each.get('room_name'))
        my_list.append(each.get('room_name'));
    print('list--->', my_list)
    list_var = tk.Variable(tab2, value=my_list)
    listbox = tk.Listbox(
        tab2,
        listvariable=list_var,
        height=6,
        selectmode=tk.EXTENDED
    )
    listbox.pack(expand=True, fill=tk.BOTH)
    listbox.bind('<<ListboxSelect>>', items_selected)


def getroomslocal():
    mycursor.execute("SELECT room_name FROM room_registered")
    myresult = mycursor.fetchall()
    array = []
    for x in myresult:
        array.append(x[0])
    print(array)
    return array


def sendmessage(value_inside, message):
    print("Selected room:", value_inside)
    print("message:", message)
    url = "http://localhost:3000/room/put_msg"

    r = requests.post(url=url, headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token_val,
    }, json={
        "key": "vjea24nr8yvwr42u56n3pwc6szmshc1p",
        "msg_type": "alert",
        "msg": message
    })
    print("JSON Response ", r.json())
    response = r.json()
    chatWindow.insert(END, "\n" + value_inside + " ->" + response['Ack'])


def getmessage(room):
    print(room)
    url = "http://localhost:3000/msg/pullMessages"

    r = requests.post(url=url, headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token_val,
    }, json={
        "room_key": "zvnfhpssgbv0blxaxdvqx4e9me81q2gt"
    })
    print("JSON Response ", r.json())
    response = r.json()
    chatWindow.insert(END, "\n" + room + " ->" + response['Ack'])


def populatetab3():
    global chatWindow
    chatWindow = Text(tab3)
    chatWindow.pack()

    # Create the list of options
    options_list = roomlist
    # Variable to keep track of the option
    # selected in OptionMenu
    value_inside = tk.StringVar()
    # Set the default value of the variable
    value_inside.set("Select an room")
    # Create the optionmenu widget and passing 
    # the options_list and value_inside to it.
    question_menu = tk.OptionMenu(tab3, value_inside, *options_list)
    question_menu.pack()

    messagelabel = tk.Label(tab3, text="Enter message here")
    messagelabel.pack()

    messageWindow = tk.Entry(tab3)
    messageWindow.pack()

    Button = tk.Button(tab3, text="Send", command=lambda: sendmessage(value_inside.get(), messageWindow.get()))
    Button.pack()

    Button1 = tk.Button(tab3, text="Get", command=lambda: getmessage(value_inside.get()))
    Button1.pack()

def storekeys(roomname,key):
    print('roomname  ',roomname)
    print('key ',key)
    
    sql = """
            UPDATE room_registered
            SET roomkey=%s
            WHERE room_name=%s
            """, (key,roomname)
    print(sql)

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) affected")

def populatetab4():
     # Create the list of options
    options_list = roomlist
    # Variable to keep track of the option
    # selected in OptionMenu
    value_inside = tk.StringVar()
    # Set the default value of the variable
    value_inside.set("Select an room")
    # Create the optionmenu widget and passing 
    # the options_list and value_inside to it.
    question_menu = tk.OptionMenu(tab4, value_inside, *options_list)
    question_menu.pack()

    messagelabel = tk.Label(tab4, text="Enter Room key")
    messagelabel.pack()

    messageWindow = tk.Entry(tab4)
    messageWindow.pack()

    Button = tk.Button(tab4, text="Send", command=lambda: storekeys(value_inside.get(), messageWindow.get()))
    Button.pack()
    
    
  
def on_tab_change(event):
    global token_val
    global roomlist
    tab = event.widget.tab('current')['text']
    if tab == 'Rooms':
        token_val = gettoken()
        if (token_val != None):
            getroomlist()
    if tab == 'messages':
        roomlist = getroomslocal()
        if (token_val != None):
            populatetab3()
    if tab == 'room keys':
         roomlist = getroomslocal()
         if (token_val != None):
             populatetab4()
        

def getchoice(roomname, choice1):
    print('mode-->', choice1)
    print('room-->', roomname)
    print(token_val)
    modeval = ''
    match choice1:
        case 'publisher':
            modeval = 0
        case 'subscriber':
            modeval = 1
        case 'both':
            modeval = 2
        case _:
            print("give correct role")

    print("final mode ", modeval)
    print(type(roomname))
    mycursor.execute("""SELECT mode  FROM room_registered WHERE room_name ='%s'""" % (roomname))
    myresult = mycursor.fetchone()
    print(myresult)
    if(myresult == None):
        url = "http://localhost:3000/room/joinRoom"
        r = requests.post(url=url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token_val,
        }, json={
            "room": roomname,
            "mode": modeval,
        })
        print("JSON Response ", r.json())
        response = r.json()
        messagebox.showinfo(response['Ack'])
        if response['Ack']:
            sql1 = "INSERT INTO room_registered (room_name,mode) VALUES (%s, %s)"
            val = (str(roomname),
                str(choice1),
                )
            print(val)
            mycursor.execute(sql1, val)

            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
    else:
        url = "http://localhost:3000/room/upgradeRole"
        r = requests.post(url=url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token_val,
        }, json={
            "room_name": roomname,
            "mode": modeval,
        })
        print("JSON Response ", r.json())
        response = r.json()
        messagebox.showinfo(response['Ack'])
        if response['Ack']:
           
            sql2 = """UPDATE room_registered SET mode = '%s' WHERE room_name = '%s'""" %(modeval,roomname)
            mycursor.execute(sql2)

            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
        
        
        
def newwin(roomname):
    win = tk.Tk()
    win.geometry('200x100')
    win.title(roomname)
    lab1 = tk.Label(win, text=roomname)
    lab1.pack()
    lab2 = tk.Label(win, text="enter sub/pub")
    lab2.pack()
     # Create the list of options
    options_list = ['publisher','subscriber','both']
    # Variable to keep track of the option
    # selected in OptionMenu
    value_inside = tk.StringVar()
    # Set the default value of the variable
    value_inside.set("Select an role")
    # Create the optionmenu widget and passing 
    # the options_list and value_inside to it.
    choice = tk.OptionMenu(win, value_inside, *options_list)
    choice.pack()
    button = tk.Button(win, text="ok", command=lambda: getchoice(roomname,value_inside.get()))
    button.pack()

    win.mainloop()


def items_selected(event):
    # get all selected indices
    global box
    selected_indices = listbox.curselection()
    # get selected items
    selected_room = ",".join([listbox.get(i) for i in selected_indices])
    msg = f'You selected: {selected_room}'
    newwin(selected_room)


tab_parent.bind('<<NotebookTabChanged>>', on_tab_change)
tab_parent.pack(expand=1, fill='both')

form.mainloop()
