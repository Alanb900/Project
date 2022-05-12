import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as messagebox
import random as rnd
import sqlite3

import socket
import threading


your_data = ""
your_choice = ""
TOTAL_NO_OF_ROUNDS = ""
your_score = 0

# network client
client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8000

#database tblUsers class
class Users:
    #create/connects to database
    def __init__(self, tablename="tblUsers", userid="Userid", username="Username", email="Email", password="Password"):
        self.__tablename=tablename
        self.__userid=userid
        self.__username=username
        self.__email=email
        self.__password=password
        conn=sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__userid + " " + " INTEGER PRIMARY KEY AUTOINCREMENT ,"
        str += " " + self.__username + " TEXT   NOT NULL ,"
        str += " " + self.__email + " TEXT   NOT NULL ,"
        str += " " + self.__password + " TEXT   NOT NULL )"
        conn.execute(str)
        print("Table created successfully")
        conn.commit()
        conn.close()

    #inserts new user to the database
    def insert_user(self, username,email,password,passwordconf):
        conn = sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        str_insert = "INSERT INTO " + self.__tablename + "(" + self.__username + "," + self.__email + "," + self.__password + ") VALUES (" + "'" + username + "'" + "," + "'" + email + "'" + "," + "'" + password + "'" + ");"
        conn.execute(str_insert)
        print("Added user successfully")
        conn.commit()
        conn.close()

    def find_user_by_username(self, username):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT Username from  " + "tblUsers" + " where " + "Username = " + "'" + str(username) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return True
        else:
            print("not selected")
            return False
        conn.commit()
        conn.close()

    def find_userid_by_username(self, username):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT Userid from  " + "tblUsers" + " where " + "Username = " + "'" + str(username) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return int(row[0])
        conn.commit()
        conn.close()

    def login(self, username, password):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT Username, Password from  " + "tblUsers" + " where " + "Username = " + "'" + str(username) + "'" + " AND Password = " +  "'" + str(password) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return True
        else:
            print("not selected")
            return False
        conn.commit()
        conn.close()

#DataBase tblGames class
class Games:
    #Cnnects to database
    def __init__(self, tablename="tblGames", gameid="Gameid", gamename="GameName", gamecode="GameCode", userid="Userid"):
        self.__tablename = tablename
        self.__gameid = gameid
        self.__gamename = gamename
        self.__gamecode = gamecode
        self.__userid = userid
        conn = sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        conn.commit()
        conn.close()

    # inserts new Game data to the database
    def insert_game(self, gamename, userid):
        conn = sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        rnd.seed()
        gamecode = rnd.randint(1000, 9999)
        check=1
        while check!=0:
            if self.check_if_gamecode_exist(gamecode) == False:
                str_insert = "INSERT INTO " + self.__tablename + "(" + self.__gamename + "," + self.__gamecode + "," + self.__userid + ") VALUES (" + "'" + str(gamename) + "'" + "," + "'" + str(gamecode) + "'" +"," + "'" + str(userid) + "'" + ");"
                conn.execute(str_insert)
                print("Created Game successfully")
                conn.commit()
                conn.close()
                check=0
                print("while end")
                return gamecode
            else:
                gamecode = rnd.randint(1000, 9999)

    def check_if_gamecode_exist(self, gamecode):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT GameCode from  " + "tblGames" + " where " + "GameCode = " + "'" + str(gamecode)  + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return True
        else:
            print("not selected")
            return False
        conn.commit()
        conn.close()

    def get_gameid_by_gamecode(self, gamecode):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT Gameid from  " + "tblGames" + " where " + "Gamecode = " + "'" + str(gamecode) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return int(row[0])
        conn.commit()
        conn.close()

    def get_all_gameid_gamename_gamecode_by_userid(self, userid):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT Gameid, GameName, GameCode from  " + "tblGames" + " where " + "Userid = " + "'" + str(userid) + "'"
        print(strsql)
        #for row in rows:
        list = []
        for row in conn.execute(strsql):
            print("selected")
            row = str(str(row[0]) + ". " + row[1] + ", " + str(row[2]))
            list.append(row)
        conn.commit()
        conn.close()
        return list

#DataBase tblQuestions Class
class Questions:
    #Cnnects to database
    def __init__(self, tablename="tblQuestions", questionname="QuestionName", questionnumber="QuestionNumber", firstanswer="FirstAnswer", secondanswer="SecondAnswer", thirdanswer="ThirdAnswer", fourthanswer="FourthAnswer", whichanswerright="WhichAnswerRight", gameid="Gameid"):
        self.__tablename = tablename
        self.__questionname = questionname
        self.__questionnumber = questionnumber
        self.__firstanswer = firstanswer
        self.__secondanswer = secondanswer
        self.__thirdanswer = thirdanswer
        self.__fourthanswer = fourthanswer
        self.__whichanswerright = whichanswerright
        self.__gameid = gameid
        conn = sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        conn.commit()
        conn.close()

    # inserts new Game data to the database
    def insert_question(self, questionname, questionnumber, firstanswer, secondanswer, thirdanswer, fourthanswer,whichanswerright, gameid):
        conn = sqlite3.connect('DataBase.db')
        print("Open data base successfully")
        str_insert = "INSERT INTO " + self.__tablename + "(" + self.__questionname + "," + self.__questionnumber + "," + self.__firstanswer + "," + self.__secondanswer + "," + self.__thirdanswer + "," + self.__fourthanswer + "," + self.__whichanswerright + "," + self.__gameid +") VALUES (" + "'" + str(questionname) + "'" + "," + "'" + str(questionnumber) + "'" + "," + "'" + str(firstanswer) + "'"  + "," + "'" + str(secondanswer) + "'" + "," + "'" + str(thirdanswer) + "'" + "," + "'" + str(fourthanswer) + "'" + "," + "'" + str(whichanswerright) + "'" + "," + "'" + str(gameid) + "'" + ");"
        conn.execute(str_insert)
        print("Created Question successfully")
        conn.commit()
        conn.close()

    def get_questiondata_by_gameid_and_questionnum(self, gameid, questionnumber):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT QuestionName, FirstAnswer, SecondAnswer, ThirdAnswer, FourthAnswer from  " + "tblQuestions" + " where " + "Gameid = " + "'" + str(gameid) + "'" + " And " + "QuestionNumber = " + "'" + str(questionnumber) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])
        conn.commit()
        conn.close()

    def get_whichanswerright_by_gameid_and_questionnum(self, gameid, questionnumber):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT WhichAnswerRight from  " + "tblQuestions" + " where " + "Gameid = " + "'" + str(gameid) + "'" + " And " + "QuestionNumber = " + "'" + str(questionnumber) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("selected")
            return int(row[0])
        conn.commit()
        conn.close()

    def checkif_questionnum_exist_by_gameid_and_questionnum(self, gameid, questionnumber):
        conn = sqlite3.connect('DataBase.db')
        print("Opened database successfully");
        strsql = "SELECT QuestionNumber from  " + "tblQuestions" + " where " + "Gameid = " + "'" + str(gameid) +  "'" + " And " + "QuestionNumber = " + "'" + str(questionnumber) + "'"
        print(strsql)
        conn.execute(strsql)
        cursor = conn.execute(strsql)
        row = cursor.fetchone()
        if row:
            print("Exists")
            return True
        else:
            print("Doesn't exist")
            return False
        conn.commit()
        conn.close()


#The welcome window
class WelcomeWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Welcome Window")
        self.label1 = Label( self, text = "Trivia Game", width = 15, height = 2, font=("david", 44))
        self.label1.grid(row = 0, column = 0, sticky = W, pady = 2)

        self.btn1 = Button(self, text = "Start", width = 5, height = 2, font=("david", 30),bg="#D3D3D3", command = self.next_Window)
        self.btn1.grid(row=1, column=0, sticky=S, pady=2)

    def next_Window(self):
        self.destroy()
        self.nextwindow = LoginRegisterWin()

#The Login/register window
class LoginRegisterWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Login Register Window")
        self.label1 = Label(self, text="Trivia Game", width=15, height=2, font=("david", 44))
        self.label1.grid(row=0, column=0, sticky=W, pady=2)

        self.btn1 = Button(self, text="Login", width=5, height=2, font=("david", 30),bg="#D3D3D3", command = self.next_window_log)
        self.btn1.grid(row=1, column=0, sticky=S, pady=2)

        self.label2 = Label(self, text="Don’t have an account?", width=0, height=2, font=("david", 12))
        self.label2.grid(row=2, column=0, sticky=S, pady=2)

        self.btn2 = Button(self, text="Register", width=0, height=2, font=("david", 12),bg="#D3D3D3", command = self.next_window_reg)
        self.btn2.grid(row=3, column=0, sticky=S, pady=2)

        self.btn3 = Button(self, text="<-- Return", width=0, height=2, font=("david", 12),bg="#D3D3D3", command=self.prev_welcome_win)
        self.btn3.grid(row=3, column=0, sticky=W, pady=2)

    def next_window_log(self):
        self.destroy()
        self.nextwindow = LoginWin()
    def next_window_reg(self):
        self.destroy()
        self.nextwindow = RegisterWin()
    def prev_welcome_win(self):
        self.destroy()
        self.prevwindow = WelcomeWin()

#The Register Form
class RegisterWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Register Window")
        self.label1 = Label(self, text="Register Window", width=0, height=2, font=("david", 30))
        self.label1.grid(row=0, column=0, sticky=W, pady=2)

        global username_var
        global email_var
        global password_var
        global passwordconf_var
        username_var = tk.StringVar()
        email_var = tk.StringVar()
        password_var = tk.StringVar()
        passwordconf_var = tk.StringVar()

        self.label2 = Label(self, text="Username:", width=0, height=2, font=("david", 30))
        self.label2.grid(row=1, column=0, sticky=W, pady=2)
        self.ent1 = Entry(self, textvariable = username_var, font=("david", 30))
        self.ent1.grid(row=1, column=1, sticky=W, pady=2)

        self.label4 = Label(self, text="Email:", width=0, height=2, font=("david", 30))
        self.label4.grid(row=3, column=0, sticky=W, pady=2)
        self.ent3 = Entry(self, textvariable = email_var, font=("david", 30))
        self.ent3.grid(row=3, column=1, sticky=W, pady=2)

        self.label5 = Label(self, text="Password:", width=0, height=2, font=("david", 30))
        self.label5.grid(row=4, column=0, sticky=W, pady=2)
        self.ent4 = Entry(self, textvariable = password_var, font=("david", 30))
        self.ent4.grid(row=4, column=1, sticky=W, pady=2)

        self.label6 = Label(self, text="Password Confirmation:", width=0, height=2, font=("david", 30))
        self.label6.grid(row=5, column=0, sticky=W, pady=2)
        self.ent5 = Entry(self, textvariable = passwordconf_var, font=("david", 30))
        self.ent5.grid(row=5, column=1, sticky=W, pady=2)

        self.btn1 = Button(self, text="<-- Return", width=0, height=2, font=("david", 12),bg="#D3D3D3", command = self.prev_logreg_win)
        self.btn1.grid(row=6, column=0, sticky=W, pady=2)

        self.btn2 = Button(self, text="Submit", width=0, height=2, font=("david", 12),bg="#D3D3D3", command = self.next_login_window)
        self.btn2.grid(row=6, column=0, sticky=E, pady=2)

    def prev_logreg_win(self):
        self.destroy()
        self.prevwindow = LoginRegisterWin()

    def next_login_window(self):
        global username_var
        global email_var
        global password_var
        global passwordconf_var
        username = username_var.get()
        email = email_var.get()
        password = password_var.get()
        passwordconf = passwordconf_var.get()
        u = Users()
        if passwordconf==password and len(username)>=1 and len(email)>=1 and len(password)>=1 and len(passwordconf)>=1:
            if u.find_user_by_username(username)==True:
                messagebox.showerror("Username taken", "Username already taken try another one.")
            else:
                u.insert_user(username, email, password, passwordconf)
                messagebox.showinfo("New user Created!", "New user was created successfuly, click 'ok' to continue to the login window.")
                self.destroy()
                self.nextwindow = LoginWin()
        elif passwordconf!=password:
            messagebox.showerror("Error!", "Password Confirmation don't match the Password.")
        else:
            messagebox.showerror("Error!", "One of the fields is missing.")

#The Login form
class LoginWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Login Window")
        self.label1 = Label(self, text="Login Window", width=0, height=2, font=("david", 30))
        self.label1.grid(row=0, column=0, sticky=W, pady=2)

        global username_var
        global password_var1
        username_var = tk.StringVar()
        password_var1 = tk.StringVar()

        self.label2 = Label(self, text="Username:", width=0, height=2, font=("david", 30))
        self.label2.grid(row=1, column=0, sticky=W, pady=2)
        self.ent1 = Entry(self, textvariable = username_var, font=("david", 30))
        self.ent1.grid(row=1, column=1, sticky=W, pady=2)

        self.label3 = Label(self, text="Password:", width=0, height=2, font=("david", 30))
        self.label3.grid(row=2, column=0, sticky=W, pady=2)
        self.ent2 = Entry(self, textvariable = password_var1, font=("david", 30))
        self.ent2.grid(row=2, column=1, sticky=W, pady=2)

        self.btn1 = Button(self, text="<-- Return", width=0, height=2, font=("david", 12),bg="#D3D3D3", command = self.prev_logreg_win)
        self.btn1.grid(row=3, column=0, sticky=W, pady=2)

        self.btn2 = Button(self, text="Submit", width=0, height=2, font=("david", 12),bg="#D3D3D3", command = self.next_main_window)
        self.btn2.grid(row=3, column=1, sticky=W, pady=2)

    def prev_logreg_win(self):
        self.destroy()
        self.prevwindow = LoginRegisterWin()

    def next_main_window(self):
        global username_var
        global password_var1
        username = username_var.get()
        password = password_var1.get()
        u=Users()
        if(len(username)>=1 and len(password)>=1):
            if Users.login(username, username, password) == True:
                messagebox.showinfo("Login Successful!", "Logged in successfuly")
                self.destroy()
                self.nextwindow = MainWin()
                self.nextwindow.labelUsername.config(text=username) #labelUsername gives easier acsess to database from each window and shows the username of the current user
            else:
                messagebox.showerror("Error!", "Username and Password don't match")
        else:
            messagebox.showerror("Error!", "Insert Username and password before procceding")

#The Main window
class MainWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Main Window")
        self.label1 = Label(self, text="Main Window", width=0, height=0, font=("david", 50))
        self.label1.grid(row=0, column=1, sticky=N, pady=20)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15),bg="#FFFF00")
        self.labelUsername.grid(row=1, column=1, sticky=N, pady=0)

        self.btn1 = Button(self, text="Join Game", width=10, height=2, font=("david", 25), bg="#D3D3D3", command = self.next_join_game_window)
        self.btn1.grid(row=2, column=1, sticky=S, pady=5)

        self.btn2 = Button(self, text="Start Game", width=10, height=2, font=("david", 25), bg="#D3D3D3", command = self.next_start_window)
        self.btn2.grid(row=3, column=1, sticky=S, pady=5)

        self.btn3 = Button(self, text="Create Game", width=10, height=2, font=("david", 25), bg="#D3D3D3", command = self.create_game_window)
        self.btn3.grid(row=4, column=1, sticky=S, pady=5)

        self.btn4 = Button(self, text="Logout", width=0, height=1, font=("david", 12), bg="#D3D3D3",command=self.logout)
        self.btn4.grid(row=5, column=1, sticky=W, pady=2)

    def next_join_game_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = JoinGameWin()
        self.NextWindow.labelUsername.config(text=username)

    def next_start_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = StartGameWin()
        self.NextWindow.labelUsername.config(text=username)

    def create_game_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = CreateGameWin()
        self.NextWindow.labelUsername.config(text=username)

    def logout(self):
        messagebox.showinfo("Logout", "You are now logged out \n Returning to Login window")
        self.destroy()
        self.PrevWindow = LoginWin()

#The Join Game window, where you can join a starting game using a unique gamecode
class JoinGameWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Join Game Window")
        self.label1 = Label(self, text="Join Game", width=0, height=0, font=("david", 30))
        self.label1.grid(row=0, column=0, sticky=W, pady=5)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15),bg="#FFFF00")
        self.labelUsername.grid(row=0, column=1, sticky=E, pady=5)

        self.label2 = Label(self, text="Enter Game Code:", width=0, height=2, font=("david", 20))
        self.label2.grid(row=1, column=0, sticky=W, pady=20)

        global gamecode_var
        gamecode_var = tk.StringVar()

        self.ent1 = Entry(self, textvariable = gamecode_var ,font=("david", 20))
        self.ent1.grid(row=1, column=1, sticky=E, pady=2)

        self.btn1 = Button(self, text="<-- Return", width=0, height=1, font=("david", 15), bg="#D3D3D3", command=self.prev_main_window)
        self.btn1.grid(row=2, column=0, sticky=W, pady=2)

        self.btn2 = Button(self, text="Join", width=0, height=1, font=("david", 15), bg="#D3D3D3", command=self.next_game_window)
        self.btn2.grid(row=2, column=0, sticky=E, pady=2)

    def connect_to_server(self, username, gamecode):
        global client, HOST_ADDR, HOST_PORT, your_data
        msg=""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_ADDR, HOST_PORT))
            your_data = str(username + ", " + gamecode + ", Joined, Unready")
            client.send(your_data.encode('utf-8'))  # Send name to server after connecting
            msg=str(client.recv(1024).decode('utf-8'))
            print(msg)
        except Exception as e:
            messagebox.showerror("Error!", "Can't connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later.")
        return msg

    def next_game_window(self):
        username=self.labelUsername.cget('text')
        global gamecode_var
        gamecode = gamecode_var.get()
        if self.connect_to_server(username, gamecode) == "Connected":
            self.destroy()
            self.NextWindow = GameWin()
            self.NextWindow.labelUsername.config(text=username)
            self.NextWindow.labelGameCode.config(text=gamecode)
            self.NextWindow.btn1.place(relx=0.789, rely=0.63, anchor='w')
            #self.NextWindow.btn2.place(relx=0.789, rely=0.78, anchor='w')
        elif self.connect_to_server(username, gamecode) == "Cant connect":
            messagebox.showerror("Error!", "Can't connect to the game.")

    def prev_main_window(self):
        username=self.labelUsername.cget("text")
        self.destroy()
        self.PrevWindow = MainWin()
        self.PrevWindow.labelUsername.config(text=username)

#The Start Game window
class StartGameWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Start Game Window")
        self.label1 = Label(self, text="Start Game", width=15, height=2, font=("david", 50))
        self.label1.grid(row=0, column=0, sticky=S, pady=0)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15), bg="#FFFF00")
        self.labelUsername.grid(row=0, column=0, sticky=E, pady=0)

        self.btn1 = Button(self, text="Choose from created", width=0, height=2, font=("david", 25), bg="#D3D3D3", command =  self.next_choose_from_window)
        self.btn1.grid(row=1, column=0, sticky=S, pady=20)

        self.btn2 = Button(self, text="Create a new game", width=0, height=2, font=("david", 25), bg="#D3D3D3", command=self.next_create_game_window)
        self.btn2.grid(row=2, column=0, sticky=S, pady=20)

        self.btn3 = Button(self, text="<-- Return", width=0, height=2, font=("david", 15), bg="#D3D3D3", command=self.prev_main_window)
        self.btn3.grid(row=3, column=0, sticky=W, pady=2)

    def next_choose_from_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = ChooseFromCreatedWin()
        self.NextWindow.labelUsername.config(text=username)

    def next_create_game_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = CreateGameWin()
        self.NextWindow.labelUsername.config(text=username)

    def prev_main_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.PrevWindow = MainWin()
        self.PrevWindow.labelUsername.config(text=username)

#The Choose from created window, where you choose the game you want to start from your selected ones, and players can join
class ChooseFromCreatedWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Choose a game Window")
        self.label1 = Label(self, text="Choose a Game", width=15, height=2, font=("david", 40))
        self.label1.grid(row=0, column=0, sticky=S, pady=0)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15), bg="#FFFF00")
        self.labelUsername.grid(row=0, column=0, sticky=E, pady=0)

        self.btn1 = Button(self, text="Show list", width=0, height=2, font=("david", 15), bg="green", command=self.games_list)
        self.btn1.grid(row=1, column=0, sticky=N, pady=2)

        self.btn2 = Button(self, text="Select", width=0, height=2, font=("david", 15), bg="#D3D3D3", state='disabled', command=self.next_game_window)
        self.btn2.grid(row=2, column=0, sticky=N, pady=5)

        self.btn3 = Button(self, text="<-- Return", width=0, height=2, font=("david", 15), bg="#D3D3D3", command=self.prev_start_game_window)
        self.btn3.grid(row=3, column=0, sticky=W, pady=2)

    #creates evreything related to gamecode
    def games_list(self):
        username = self.labelUsername.cget('text')
        userid=Users().find_userid_by_username(username)
        langs=Games().get_all_gameid_gamename_gamecode_by_userid(userid)

        # create a list box
        langs_var = tk.StringVar(value=langs)
        self.listbox = tk.Listbox(self, listvariable=langs_var, height=20, width=100, selectmode='extended')
        self.listbox.grid(row=1, column=0, sticky='nwes')
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        #create gamecode label for easier use
        self.labelGameCode = Label(self, width=0, height=0, font=("david", 15), bg="red")
        self.labelGameCode.place(relx=0.93, rely=0.16, anchor='w')

        self.btn1.config(state='disabled')
        self.btn1.grid_remove()
        self.btn2.config(state='normal')

    #function that shows what you clicked on a list
    def items_selected(self, event):
        """ handle item selected event"""
        # get selected indices
        selected_indices = self.listbox.curselection()
        # get selected items
        selected_langs = ",".join([self.listbox.get(i) for i in selected_indices])
        if selected_langs:
            selected_langs = selected_langs.split(", ",1)[1]
            self.labelGameCode.config(text=selected_langs)
        else:
            messagebox.showerror("Error!", "You didnt create any games yet.")

    def connect_to_server(self, username, gamecode):
        global client, HOST_ADDR, HOST_PORT, your_data
        msg=""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_ADDR, HOST_PORT))
            your_data=str(username + ", " + gamecode + ", Created, Unstarted")
            client.send(your_data.encode('utf-8'))  # Send name to server after connecting
            msg="Connected"
        except Exception as e:
            msg="Cant Connect"
            messagebox.showerror("Error!", "Can't connect to host: " + HOST_ADDR + "on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later.")
        return msg

    def next_game_window(self):
        username = self.labelUsername.cget("text")
        gamecode=self.labelGameCode.cget("text")
        if gamecode!="":
            if self.connect_to_server(username, gamecode) == "Connected":
                self.destroy()
                self.NextWindow = GameWin()
                self.NextWindow.labelUsername.config(text=username)
                self.NextWindow.labelGameCode.config(text=gamecode)
                self.NextWindow.btn3.place(relx=0.789, rely=0.93, anchor='w')
                self.NextWindow.btn4.place(relx=0.789, rely=0.8, anchor='w')
                """self.NextWindow.scrollBar.place(relx=0.93, rely=0.68, anchor='w')
                self.NextWindow.tkDisplay.place(relx=0.72, rely=0.68, anchor='w')
                self.NextWindow.refreshbtn.place(relx=0.955, rely=0.685, anchor='w')"""
        else:
            messagebox.showerror("Error!", "Select a game before proceeding")

    def prev_start_game_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.PrevWindow = StartGameWin()
        self.PrevWindow.labelUsername.config(text=username)

#The Create Game Window, where you can create a new game that will get his unique game code between 1000-9999
class CreateGameWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Create Game Window")
        self.label1 = Label(self, text="Create Game", width=0, height=2, font=("david", 30))
        self.label1.grid(row=0, column=1, sticky=W, pady=0)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15), bg="#FFFF00")
        self.labelUsername.grid(row=0, column=1, sticky=E, pady=0)

        # asks for game name from user puts in the database and genartes unique game code between 1000-9999
        self.label2 = Label(self, text="Enter Games's name: ", width=0, height=0, font=("david", 20), bg="dark grey")
        self.label2.grid(row=1, column=0, sticky=W, pady=0)
        global game_name_var
        game_name_var = tk.StringVar()
        self.ent1 = Entry(self, textvariable = game_name_var, font=("david", 20), width=25)
        self.ent1.grid(row=1, column=1, sticky=W, pady=2)
        self.btn1 = Button(self, text="Continue", width=0, height=2, font=("david", 10), bg="#D3D3D3", command=self.create_game_in_db)
        self.btn1.grid(row=1, column=1, sticky=E, pady=10)
        self.labelGamecode = Label(self, text="Game code: ", width=0, height=0, font=("david", 15))
        self.labelGamecode.place(relx=0, rely=0.12, anchor='w')
        self.labelTheGamecode = Label(self, width=0, height=0, font=("david", 15), bg="red")
        self.labelTheGamecode.place(relx=0.152, rely=0.12, anchor='w')

        global question_name_var
        global first_answer_var
        global second_answer_var
        global third_answer_var
        global fourth_answer_var
        question_name_var = tk.StringVar()
        first_answer_var = tk.StringVar()
        second_answer_var = tk.StringVar()
        third_answer_var = tk.StringVar()
        fourth_answer_var = tk.StringVar()

        self.Questionnum=1
        self.label3 = Label(self, text="Question number " + str(self.Questionnum) + ":", width=15, height=0, font=("david", 20))
        self.label3.grid(row=2, column=0, sticky=E, pady=2)

        self.ent2 = Entry(self, textvariable= question_name_var,font=("david", 20), width= 35, state='disabled')
        self.ent2.grid(row=2, column=1, sticky=W, pady=2)

        #1st answer design
        self.btn2 = Button(self, text="       ", width=0, height=2, font=("david", 10), bg="white", state='disabled', command=self.btn2_color)
        self.btn2.grid(row=3, column=0, sticky=W, pady=20)
        self.label4 = Label(self, text="1st answer: ", width=0, height=0, font=("david", 20))
        self.label4.place(relx = 0.05, rely = 0.34, anchor = 'w')
        self.ent3 = Entry(self, textvariable= first_answer_var, font=("david", 20), width=35, state='disabled')
        self.ent3.grid(row=3, column=1, sticky=W, pady=2)

        #2nd answer design
        self.btn3 = Button(self, text="       ", width=0, height=2, font=("david", 10), bg="white", state='disabled', command=self.btn3_color)
        self.btn3.grid(row=4, column=0, sticky=W, pady=20)
        self.label5 = Label(self, text="2nd answer: ", width=0, height=0, font=("david", 20))
        self.label5.place(relx=0.05, rely=0.46, anchor='w')
        self.ent4 = Entry(self, textvariable= second_answer_var, font=("david", 20), width=35, state='disabled')
        self.ent4.grid(row=4, column=1, sticky=W, pady=2)

        #3rd answer design
        self.btn4 = Button(self, text="       ", width=0, height=2, font=("david", 10), bg="white", state='disabled', command=self.btn4_color)
        self.btn4.grid(row=5, column=0, sticky=W, pady=20)
        self.label6 = Label(self, text="3rd answer: ", width=0, height=0, font=("david", 20))
        self.label6.place(relx=0.05, rely=0.58, anchor='w')
        self.ent5 = Entry(self, textvariable= third_answer_var, font=("david", 20), width=35, state='disabled')
        self.ent5.grid(row=5, column=1, sticky=W, pady=2)

        #4th answer design
        self.btn5 = Button(self, text="       ", width=0, height=2, font=("david", 10), bg="white", state='disabled', command=self.btn5_color)
        self.btn5.grid(row=6, column=0, sticky=W, pady=20)
        self.label7 = Label(self, text="4th answer: ", width=0, height=0, font=("david", 20))
        self.label7.place(relx=0.05, rely=0.7, anchor='w')
        self.ent6 = Entry(self, textvariable= fourth_answer_var, font=("david", 20), width=35, state='disabled')
        self.ent6.grid(row=6, column=1, sticky=W, pady=2)

        self.btn6 = Button(self, text="Add another question", width=17, height=2, font=("david", 15), bg="#D3D3D3", state='disabled', command=self.create_question_in_db)
        self.btn6.grid(row=7, column=1, sticky=W, pady=10)

        self.btn7 = Button(self, text="Create", width=17, height=2, font=("david", 15), bg="#D3D3D3", state='disabled', command=self.create_game_and_prev_main_window)
        self.btn7.grid(row=8, column=1, sticky=W, pady=10)

        self.btn8 = Button(self, text="<-- return", width=0, height=2, font=("david", 15), bg="#D3D3D3", command=self.prev_main_window)
        self.btn8.grid(row=8, column=0, sticky=W, pady=2)

    def create_game_in_db(self):
        global game_name_var
        gamename = game_name_var.get()
        if(len(gamename)>=1):
            g=Games()
            u=Users()
            username = self.labelUsername.cget("text")
            userid = u.find_userid_by_username(username)
            gamecode = g.insert_game(str(gamename), userid)
            self.labelTheGamecode.config(text=gamecode)
            self.ent1.config(state = 'disabled')
            self.btn1.config(state = 'disabled')
            self.btn8.config(state = 'disabled')
            self.ent2.config(state='normal')
            self.ent3.config(state='normal')
            self.ent4.config(state='normal')
            self.ent5.config(state='normal')
            self.ent6.config(state='normal')
            self.btn2.config(state='active')
            self.btn3.config(state='active')
            self.btn4.config(state='active')
            self.btn5.config(state='active')
            self.btn6.config(state='active')
            self.btn7.config(state='active')

#changes the colors for all 4 answer buttons to set which one is the "right" one
    def btn2_color(self):
        if self.btn2['bg']=="white" and self.btn3['bg']!="red" and self.btn4['bg']!="red" and self.btn5['bg']!="red":
            self.btn2['bg']="red"
        elif self.btn2['bg']=="red":
            self.btn2['bg']="white"
    def btn3_color(self):
        if self.btn3['bg']=="white" and self.btn2['bg']!="red" and self.btn4['bg']!="red" and self.btn5['bg']!="red":
            self.btn3['bg']="red"
        elif self.btn3['bg']=="red":
            self.btn3['bg']="white"
    def btn4_color(self):
        if self.btn4['bg']=="white" and self.btn2['bg']!="red" and self.btn3['bg']!="red" and self.btn5['bg']!="red":
            self.btn4['bg']="red"
        elif self.btn4['bg']=="red":
            self.btn4['bg']="white"
    def btn5_color(self):
        if self.btn5['bg']=="white" and self.btn2['bg']!="red" and self.btn3['bg']!="red" and self.btn4['bg']!="red":
            self.btn5['bg']="red"
        elif self.btn5['bg']=="red":
            self.btn5['bg']="white"

    #creates a new question in the db after clicking "add a new question"
    def create_question_in_db(self):
        global question_name_var
        global first_answer_var
        global second_answer_var
        global third_answer_var
        global fourth_answer_var
        questionname = question_name_var.get()
        firstanswer = first_answer_var.get()
        secondanswer = second_answer_var.get()
        thirdanswer = third_answer_var.get()
        fourthanswer = fourth_answer_var.get()
        if len(questionname)>=1 and len(firstanswer)>=1 and len(secondanswer)>=1 and len(thirdanswer)>=1 and len(fourthanswer)>=1 and (self.btn2['bg']=="red" or self.btn3['bg']=="red" or self.btn4['bg']=="red" or self.btn5['bg']=="red"):
            btnnum=0
            if self.btn2['bg']=="red":
                btnnum=1
            elif self.btn3['bg']=="red":
                btnnum=2
            elif self.btn4['bg']=="red":
                btnnum=3
            elif self.btn5['bg']=="red":
                btnnum=4
            q=Questions()
            gamecode=self.labelTheGamecode.cget("text")
            g=Games()
            gameid=g.get_gameid_by_gamecode(gamecode)
            q.insert_question(questionname,self.Questionnum,firstanswer,secondanswer,thirdanswer,fourthanswer,btnnum,gameid)
            self.Questionnum+=1
            self.label3.config(text="Question number " + str(self.Questionnum)) #updates question num
            #resets text that were typed to entrys
            self.ent2.delete(0,END)
            self.ent3.delete(0, END)
            self.ent4.delete(0, END)
            self.ent5.delete(0, END)
            self.ent6.delete(0, END)
            #resets buttons colors
            self.btn2['bg'] = "white"
            self.btn3['bg'] = "white"
            self.btn4['bg'] = "white"
            self.btn5['bg'] = "white"

    def create_game_and_prev_main_window(self):
        username = self.labelUsername.cget("text")
        messagebox.showinfo("Game created!", "The game was created successfuly! \n Returning to the Main window")
        self.destroy()
        self.PrevWindow = MainWin()
        self.PrevWindow.labelUsername.config(text=username)

    def prev_main_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.PrevWindow = MainWin()
        self.PrevWindow.labelUsername.config(text=username)

#The Game Window, where you can play the game, if you have the status of "game cretor" than you can start the game while others that joined are playing
#And if you have the status of "joined game", than you can play the game that other user created, and playing vs other players that have joined the same game
class GameWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Game Window")

        self.l1 = Label(self, text=" ", width=0, height=2, font=("david", 60))
        self.l1.grid(row=0, column=2, sticky=N, pady=0)

        self.label1 = Label(self, text="Game Window", width=0, height=2, font=("david", 40))
        self.label1.place(relx=0.22, rely=0.1, anchor='w')

        self.labelGameCode = Label(self, width=0, height=0, font=("david", 15), bg="red")
        self.labelGameCode.place(relx=0, rely=0.1, anchor='w')

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15), bg="#FFFF00")
        self.labelUsername.grid(row=0, column=0, sticky=W, pady=0)

        self.l2 = Label(self, text=" ", width=0, height=2, font=("david", 30))
        self.l2.grid(row=2, column=1, sticky=N, pady=0)

        questionnum = 1
        self.labelQuestionNum = Label(self, text= str(questionnum), width=0, height=2, font=("david", 22))
        self.labelQuestionNum.place(relx=0.0, rely=0.3, anchor='w')

        self.labelQuestion = Label(self, width=0, height=0, font=("david", 22), bg="#999999")
        self.labelQuestion.place(relx=0.05, rely=0.3, anchor='w')

        self.firstAnswer = Button(self, text="1st answer", width=30, height=6, font=("david", 15), bg="#ED1C24", state='disabled', command=self.firstanswerchoice)
        self.firstAnswer.grid(row=2, column=0, sticky=E, pady=0)
        self.secondAnswer = Button(self, text="2nd answer", width=30, height=6, font=("david", 15), bg="light blue", state='disabled', command=self.secondanswerchoice)
        self.secondAnswer.grid(row=2, column=1, sticky=W, pady=0)
        self.thirdAnswer = Button(self, text="3rd answer", width=30, height=6, font=("david", 15), bg="#3CB043", state='disabled', command=self.thirdanswerchoice)
        self.thirdAnswer.grid(row=3, column=0, sticky=E, pady=0)
        self.fourthAnswer = Button(self, text="4th answer", width=30, height=6, font=("david", 15), bg="#EFFD5F", state='disabled', command=self.fourthanswerchoice)
        self.fourthAnswer.grid(row=3, column=1, sticky=W, pady=0)

        self.labelScore = Label(self, text="Your Score:", width=0, height=0, font=("david", 15))
        self.labelScore.place(relx=0.78, rely=0.08, anchor='w')
        score=0
        self.labelScoreNum = Label(self,text= score, width=0, height=0, font=("david", 15), bg="#D3D3D3")
        self.labelScoreNum.place(relx=0.9, rely=0.08, anchor='w')

        #the leaderboard
        self.labelLeaderboard = Label(self, text="Leaderboard:", width=15, height=0, font=("david", 25))
        self.labelLeaderboard.grid(row=0, column=2, sticky=W, pady=0)

        self.labelFirstPlace = Label(self, text="First Place:", width=0, height=0, font=("david", 15))
        self.labelFirstPlace.place(relx=0.72, rely=0.28, anchor='w')
        self.labelFirstPlaceName = Label(self, width=0, height=0, font=("david", 15), bg="#D3D3D3")
        self.labelFirstPlaceName.place(relx=0.82, rely=0.28, anchor='w')

        self.labelSecondPlace = Label(self, text="Second Place:", width=0, height=0, font=("david", 15))
        self.labelSecondPlace.place(relx=0.72, rely=0.38, anchor='w')
        self.labelSecondPlaceName = Label(self, width=0, height=0, font=("david", 15), bg="#D3D3D3")
        self.labelSecondPlaceName.place(relx=0.84, rely=0.38, anchor='w')

        self.labelThirdPlace = Label(self, text="Third Place:", width=0, height=0, font=("david", 15))
        self.labelThirdPlace.place(relx=0.72, rely=0.48, anchor='w')
        self.labelThirdPlaceName = Label(self, width=0, height=0, font=("david", 15), bg="#D3D3D3")
        self.labelThirdPlaceName.place(relx=0.83, rely=0.48, anchor='w')

        self.btn1 = Button(self, text="Ready", width=10, height=2, font=("david", 15), bg="#D3D3D3", command=self.ready_to_play)
        self.btn1.place_forget()
        #self.btn2 = Button(self, text="Unready", width=10, height=2, font=("david", 15), bg="#D3D3D3", command=self.unready_to_play, state='disabled')
        #self.btn2.place_forget()
        self.btn3 = Button(self, text="Start", width=10, height=2, font=("david", 15), bg="#D3D3D3", command=self.start_game)
        self.btn3.place_forget()
        self.btn4= Button(self, text="Next Question", width=10, height=2, font=("david", 15), bg="#D3D3D3", state='disabled',command=self.next_question)
        self.btn4.place_forget()
        self.btn5 = Button(self, text="Countinue", width=10, height=2, font=("david", 15), bg="#D3D3D3",command=self.end_game)
        self.btn5.place_forget()

        """self.scrollBar = tk.Scrollbar(self)
        self.tkDisplay = tk.Text(self, height=8, width=29, font=("david", 12))
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        self.scrollBar.place_forget()
        self.tkDisplay.place_forget()
        self.refreshbtn=Button(self, text="R", width=0, height=0, font=("david", 12), bg="#D3D3D3", command=self.insert_current_joined_users_to_display)
        self.refreshbtn.place_forget()"""

        self.separator=ttk.Separator(self, orient='vertical')
        self.separator.place(relx=0.71, rely=0, relheight=1, relwidth=0.01)

        self.answer= self.labelSecondPlace = Label(self, text="", width=0, height=0, font=("david", 15))
        self.answer.place_forget()

    """def insert_current_joined_users_to_display(self):
        global client
        gamecode = self.labelGameCode.cget("text")
        sndmsg = "Get users, " + gamecode
        client.send(sndmsg.encode('utf-8'))
        rcvmsg = str(client.recv(1024).decode('utf-8'))
        name_list =[]
        rcvmsg = rcvmsg.split("']")[0]
        rcvmsg = rcvmsg.split("', '")
        for r in rcvmsg:
            name_list.append(r)
        self.tkDisplay.config(state=tk.NORMAL)
        self.tkDisplay.delete('1.0', tk.END)
        for c in name_list:
            self.tkDisplay.insert(tk.END, c + "\n")
        self.tkDisplay.config(state=tk.DISABLED)"""

    """def unready_to_play(self):
        global client
        sndmsg = str("Unready, " + your_data.split(", ", 1)[0])
        client.send(sndmsg.encode('utf-8'))
        print(sndmsg)
        self.btn1['state'] = 'normal'
        self.btn2['state'] = 'disabled'"""

    def ready_to_play(self):
        global client
        sndmsg = str("Ready, " + your_data.split(", ", 1)[0])
        client.send(sndmsg.encode('utf-8'))
        print(sndmsg)
        self.btn1['state']= 'disabled'
        #self.btn2['state'] = 'normal'
        threading._start_new_thread(self.start_game_for_joined_player, (client, "m"))

    def start_game_for_joined_player(self, sckt, m): #showing the same game to all users with the same gamecode
        client.send("ready".encode('utf-8'))
        while True:
            from_server = sckt.recv(1024).decode('utf-8')
            if str(from_server)=="Start":
                self.set_gamedata("normal")
                #threading._start_new_thread(self.set_gamedata,("normal"))
                break
            #if str(from_server)=="Cant start":
                #self.btn1['state']= 'normal'

    def start_game(self):
        global client
        sndmsg = str("Can start?, " + your_data.split(", ", 1)[0])
        client.send(sndmsg.encode('utf-8'))
        print(sndmsg)
        rcvmsg = str(client.recv(1024).decode('utf-8'))
        print(rcvmsg)
        if rcvmsg == "Start":
            #self.refreshbtn['state']='diasbled'
            self.set_gamedata("disabled")
            self.btn4['state'] = 'normal'
            #threading._start_new_thread(self.set_gamedata,("disabled"))
        elif rcvmsg == "Cant start":
            messagebox.showerror("Error!", "Can't start, waiting for another players to connect")

    def next_question(self):
        global client
        sndmsg = str("Next question?")
        client.send(sndmsg.encode('utf-8'))
        print(sndmsg)
        rcvmsg = str(client.recv(1024).decode('utf-8'))
        print(rcvmsg)
        if rcvmsg == "Continue":
            #self.refreshbtn['state']='diasbled'
            questionnum = int(self.labelQuestionNum.cget("text"))
            questionnum+=1
            self.labelQuestionNum.config(text=questionnum)
            gamecode = self.labelGameCode.cget("text")
            gameid = Games().get_gameid_by_gamecode(gamecode)
            questionnum = self.labelQuestionNum.cget("text")

            self.procced_to_nextQuestion_ifExists_for_GameCreator(gameid,questionnum)
            #threading._start_new_thread(self.set_gamedata,("normal"))
        elif rcvmsg == "Cant procced":
            messagebox.showerror("Error!", "Can't procced, waiting for another players to answer")

    def firstanswerchoice(self):
        self.game_logic(1)
        self.set_gamedata("disabled")
        self.answer['text']="Pending.."
        self.answer['bg']="light grey"
        self.answer.place(relx=0.78, rely=0.83, anchor='w')

    def secondanswerchoice(self):
        self.game_logic(2)
        self.set_gamedata("disabled")
        self.answer['text'] = "Pending.."
        self.answer['bg'] = "light grey"
        self.answer.place(relx=0.78, rely=0.83, anchor='w')

    def thirdanswerchoice(self):
        self.game_logic(3)
        self.set_gamedata("disabled")
        self.answer['text'] = "Pending.."
        self.answer['bg'] = "light grey"
        self.answer.place(relx=0.78, rely=0.83, anchor='w')

    def fourthanswerchoice(self):
        self.game_logic(4)
        self.set_gamedata("disabled")
        self.answer['text'] = "Pending.."
        self.answer['bg'] = "light grey"
        self.answer.place(relx=0.78, rely=0.83, anchor='w')

    def game_logic(self, playerschoice):
        global your_choice, your_score, client
        your_choice = playerschoice

        gamecode = self.labelGameCode.cget("text")
        gameid = Games().get_gameid_by_gamecode(gamecode)

        questionnum = self.labelQuestionNum.cget("text")

        whichAnswerRight = Questions().get_whichanswerright_by_gameid_and_questionnum(gameid, questionnum)

        threading._start_new_thread(self.next_question_for_joined_player, (client, whichAnswerRight, gameid, questionnum))

    def next_question_for_joined_player(self, sckt, whichAnswerRight, gameid, questionnum):
        global your_choice, your_score, client
        client.send("answer".encode('utf-8'))
        while True:
            from_server = client.recv(1024).decode('utf-8')
            if whichAnswerRight == your_choice and from_server == "Continue":
                your_score += 1
                self.answer.config(text="Anwser is Right", bg="green")
                self.labelScoreNum.config(text=your_score)
                self.procced_to_nextQuestion_ifExists(gameid, questionnum, your_score)
                break

            elif whichAnswerRight != your_choice and from_server == "Continue":
                self.answer.config(text="Anwser is Wrong", bg="red")
                score = self.labelScoreNum.cget('text')
                self.procced_to_nextQuestion_ifExists(gameid, questionnum, your_score)
                break

    def set_gamedata(self, btnstate):
        gamecode= self.labelGameCode.cget("text")
        gameid=Games().get_gameid_by_gamecode(gamecode)
        questionnum=self.labelQuestionNum.cget("text")
        questionname, firstanswer, secondanswer, thirdanswer, fourthanswer =Questions().get_questiondata_by_gameid_and_questionnum(gameid, questionnum)
        self.labelQuestion['text'] = questionname
        if btnstate=="normal":
            self.firstAnswer.config(text= "1. " + firstanswer, state='normal')
            self.secondAnswer.config(text= "2. " + secondanswer, state='normal')
            self.thirdAnswer.config(text= "3. " + thirdanswer, state='normal')
            self.fourthAnswer.config(text= "4. " + fourthanswer, state='normal')
        if btnstate=="disabled":
            self.firstAnswer.config(text= "1. " + firstanswer, state='disabled')
            self.secondAnswer.config(text= "2. " + secondanswer, state='disabled')
            self.thirdAnswer.config(text= "3. " + thirdanswer, state='disabled')
            self.fourthAnswer.config(text= "4. " + fourthanswer, state='disabled')
        self.btn3.config(state='disabled')

    def procced_to_nextQuestion_ifExists(self, gameid, questionnum, score):
        questionnum = int(self.labelQuestionNum.cget('text'))
        questionnum += 1
        if Questions.checkif_questionnum_exist_by_gameid_and_questionnum(gameid, gameid, questionnum) == True:
            self.labelQuestionNum.config(text=questionnum)
            self.set_gamedata("normal")
        else:
            self.answer['text'] = "Game over, your score is: " + str(score)
            self.answer['bg'] = "light grey"
            self.answer['font'] = ("david", 12)
            self.answer.place(relx=0.75, rely=0.8, anchor='w')
            self.btn5.place(relx=0.789, rely=0.93, anchor='w')

    def procced_to_nextQuestion_ifExists_for_GameCreator(self, gameid, questionnum):
        global client
        if Questions.checkif_questionnum_exist_by_gameid_and_questionnum(gameid, gameid, questionnum) == True:
            self.labelQuestionNum.config(text=questionnum)
            self.set_gamedata("disabled")
        else:
            self.answer['text'] = "Game is over"
            self.answer['bg'] = "light grey"
            self.answer['font'] = ("david", 12)
            self.answer.place(relx=0.805, rely=0.8, anchor='w')
            self.btn4.place_forget()
            self.btn5.place(relx=0.789, rely=0.93, anchor='w')

    def end_game(self):
        sndmsg = str("End game")
        client.send(sndmsg.encode('utf-8'))
        self.next_LeaderBoard_window()

    def next_LeaderBoard_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = LeaderBoardWin()
        self.NextWindow.labelUsername.config(text=username)

#The LeaderBoard Window, after the game is over, it procceds to the leaderboard window where you can see the top 5 Users in the leaderboard
class LeaderBoardWin(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("LeaderBoard Window")

        self.label1 = Label(self, text="LeaderBoard Window", width=0, height=2, font=("david", 40))
        self.label1.grid(row=0, column=0, sticky=N, pady=0)

        self.labelUsername = Label(self, width=0, height=0, font=("david", 15), bg="#FFFF00")
        self.labelUsername.grid(row=0, column=1, sticky=E, pady=0)

        self.labelFirstPlace = Label(self, text="First Place: ", width=0, height=2, font=("david", 15))
        self.labelFirstPlace.grid(row=1, column=0, sticky=W, pady=0)
        self.labelFirstPlaceData = Label(self, width=0, height=0, font=("david", 15), bg="#9e9e9e")
        self.labelFirstPlaceData.place(relx=0.2, rely=0.34, anchor='w')

        self.labelSecondPlace = Label(self, text="Second Place: ", width=0, height=2, font=("david", 15))
        self.labelSecondPlace.grid(row=2, column=0, sticky=W, pady=0)
        self.labelSecondPlaceData = Label(self, width=0, height=0, font=("david", 15), bg="#8e8e8e")
        self.labelSecondPlaceData.place(relx=0.24, rely=0.45, anchor='w')

        self.labelThirdPlace = Label(self, text="Third Place: ", width=0, height=2, font=("david", 15))
        self.labelThirdPlace.grid(row=3, column=0, sticky=W, pady=0)
        self.labelThirdPlaceData = Label(self, width=0, height=0, font=("david", 15), bg="#7e7e7e")
        self.labelThirdPlaceData.place(relx=0.21, rely=0.57, anchor='w')

        self.labelFourthPlace = Label(self, text="Fourth Place: ", width=0, height=2, font=("david", 15))
        self.labelFourthPlace.grid(row=4, column=0, sticky=W, pady=0)
        self.labelFourthPlaceData = Label(self, width=0, height=0, font=("david", 15), bg="#6f6f6f")
        self.labelFourthPlaceData.place(relx=0.23, rely=0.68, anchor='w')

        self.labelFifthPlace = Label(self, text="Fifth Place: ", width=0, height=2, font=("david", 15))
        self.labelFifthPlace.grid(row=5, column=0, sticky=W, pady=0)
        self.labelFifthPlaceData = Label(self, width=0, height=0, font=("david", 15), bg="#5f5f5f")
        self.labelFifthPlaceData.place(relx=0.2, rely=0.8, anchor='w')

        self.btn1 = Button(self, text="Continue", width=10, height=2, font=("david", 15), bg="#D3D3D3", command=self.next_main_window)
        self.btn1.grid(row=6, column=0, sticky=S, pady=0)

    def next_main_window(self):
        username = self.labelUsername.cget("text")
        self.destroy()
        self.NextWindow = MainWin()
        self.NextWindow.labelUsername.config(text=username)

def main():
    WelcomeWin().mainloop()
if __name__ == '__main__':
    main()