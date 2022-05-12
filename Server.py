import tkinter as tk
import socket
import threading
from time import sleep

window = tk.Tk()
window.title("Server")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda: start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text="Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text="Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

server = None
HOST_ADDR = '0.0.0.0'
HOST_PORT = 8000
client_data = " "
clients = []
clients_connection_type = []
player_data = []
answer_data = []
score_data = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(10)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    global client_data
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, clients_connection_type, client_data, clients, player_data, answer_data, score_data

    client_data = str(client_connection.recv(1024).decode('utf-8'))
    connType = client_data.split(", ", 3)[2]
    gamecode = client_data.split(", ", 3)[1]
    username = client_data.split(", ", 3)[0]
    if connType == "Created":
        clients_connection_type.append(client_data)
        insert_client_data_to_display(clients_connection_type)  # update client names display
    elif connType == "Joined" and get_if_username_already_exists(clients_connection_type,
                                                                 username) == False and get_if_gamecode_already_exists(
            clients_connection_type,
            gamecode) == True:  # checks if the user that tries to join already exists and if not, than if the user uses valid gamecode of already existing and pending game
        msg = "Connected"
        client_connection.send(msg.encode('utf-8'))  # send message to the client that he connected to the game
        clients_connection_type.append(client_data)
        insert_client_data_to_display(clients_connection_type)  # update client names display
    else:
        msg = "Cant connect"
        client_connection.send(msg.encode('utf-8'))  # send message to the client that he cant connect to the game

    while True:
        data = str(client_connection.recv(1024).decode('utf-8'))
        print(data)
        if not data: break

        if data.startswith("Ready"):  # updats in the server if the user is ready to play
            for c in clients_connection_type:
                i = clients_connection_type.index(c)
                username = data.split(", ", 2)[1]
                currentuser = str(c)
                currentusername = c.split(", ", 1)[0]
                if currentusername == username:
                    currentuser = currentuser.split(", ", 3)
                    currentuser = str(currentuser[0] + ", " + currentuser[1] + ", " + currentuser[2] + ", Ready")
                    userisready = currentuser
                    clients_connection_type[i] = userisready
            insert_client_data_to_display(clients_connection_type)

        elif data.startswith("Unready"):  # updats in the server if the user is unready to play
            for c in clients_connection_type:
                i = clients_connection_type.index(c)
                username = data.split(", ", 2)[1]
                currentuser = str(c)
                currentusername = c.split(", ", 1)[0]
                if currentusername == username:
                    currentuser = currentuser.split(", ", 3)
                    currentuser = str(currentuser[0] + ", " + currentuser[1] + ", " + currentuser[2] + ", Unready")
                    userisready = currentuser
                    clients_connection_type[i] = userisready
            insert_client_data_to_display(clients_connection_type)

        if data.startswith("Get users"):
            newGamecode = data.split(", ", 1)[1]
            print(newGamecode)
            list = []
            for c in clients_connection_type:
                currentuser = str(c)
                currentgamecode = str(c.split(", ", 2)[1])
                isjoined = str(c.split(", ", 2)[2])
                print(isjoined)
                if currentgamecode == newGamecode and isjoined.startswith("Joined"):
                    currentuser = currentuser.split(", ", 3)
                    currentuser = str(currentuser[0] + ", " + currentuser[2] + ", " + currentuser[3])
                    list.append(currentuser)
            msg = str(list)
            client_connection.send(msg.encode('utf-8'))

        # if get_num_of_joined_players_in_game(clients_connection_type, gamecode) > 1 and data == "Can start?":
        # msg = "Start"
        # client_connection.send(msg.encode('utf-8'))  # send message to the client that he cant connect to the game

        if get_num_of_joined_players_in_game(clients_connection_type, gamecode) > 1 and is_game_started(clients_connection_type, gamecode) < 1:  # showing the same game to all users with the same gamecode
            numofplayers = get_num_of_joined_players_in_game(clients_connection_type, gamecode)
            if data.startswith("ready"):
                getmsg = {"socket": client_connection}

                if len(player_data) < (numofplayers):
                    player_data.append(getmsg)

            if len(player_data) == (numofplayers) and data.startswith("Can start?"):
                print(player_data)
                i = 0
                for p in player_data:
                    player_data[i].get("socket").send("Start".encode('utf-8'))
                    i += 1
                client_connection.send("Start".encode('utf-8'))

                for c in clients_connection_type: #means the game have started
                    i = clients_connection_type.index(c)
                    username = data.split(", ", 2)[1]
                    currentuser = str(c)
                    currentusername = c.split(", ", 1)[0]
                    if currentusername == username:
                        currentuser = currentuser.split(", ", 3)
                        currentuser = str(currentuser[0] + ", " + currentuser[1] + ", " + currentuser[2] + ", Started")
                        userisready = currentuser
                        clients_connection_type[i] = userisready
                insert_client_data_to_display(clients_connection_type)

                # player_data = []
                # return False
            else:
                msg = "Cant start"
                client_connection.send(msg.encode('utf-8'))
                # player_data=[]

        elif data == "Can start?":
            msg = "Cant start"
            client_connection.send(msg.encode('utf-8'))  # send message to the client that he cant connect to the game

        if data=="End game":
            idx = get_client_index(clients, client_connection)
            del clients_connection_type[idx]
            del clients[idx]
            player_data = []
            answer_data = []
            score_data = []
            client_connection.close()
            insert_client_data_to_display(clients_connection_type)
            break

        if get_num_of_joined_and_ready_players_in_game(clients_connection_type,gamecode) > 1 and is_game_started(clients_connection_type, gamecode) ==1:
            numofplayers = get_num_of_joined_players_in_game(clients_connection_type, gamecode)
            if data.startswith("answer"):
                getmsg1 = {"socket": client_connection}

                if len(answer_data) < (numofplayers):
                    answer_data.append(getmsg1)

            if len(answer_data) == (numofplayers) and data == "Next question?":
                i = 0
                for p in answer_data:
                    player_data[i].get("socket").send("Continue".encode('utf-8'))
                    i += 1
                client_connection.send("Continue".encode('utf-8'))
                answer_data = []

            elif data == "Next question?":
                msg = "Cant procced"
                client_connection.send(
                    msg.encode('utf-8'))  # send message to the client that he cant procced to the game


def get_if_gamecode_already_exists(client_connection_type_list, gamecode):
    for c in client_connection_type_list:
        c = str(c)
        gamecodeexists = c.split(", ", 2)[1]
        if gamecodeexists == gamecode:
            return True
    return False


def get_if_username_already_exists(client_connection_type_list, username):
    for c in client_connection_type_list:
        c = str(c)
        usernameexists = c.split(", ", 2)[0]
        if usernameexists == username:
            return True
    return False


def get_num_of_joined_players_in_game(client_connection_type_list, gamecode):
    i = 0
    for c in client_connection_type_list:
        c = str(c)
        gamecodeexists = c.split(", ", 2)[1]
        status = c.split(", ", 2)[2]
        if gamecodeexists == gamecode and status.startswith("Joined"):
            i += 1
    return i


def get_num_of_joined_and_ready_players_in_game(client_connection_type_list, gamecode):
    i = 0
    for c in client_connection_type_list:
        c = str(c)
        gamecodeexists = c.split(", ", 2)[1]
        status = c.split(", ", 2)[2]
        ready = ""
        if status != "Created":
            ready = status.split(", ")[1]
        if gamecodeexists == gamecode and status.startswith("Joined") and ready == "Ready":
            i += 1
    return i

def is_game_started(client_connection_type_list, gamecode):
    i = 0
    for c in client_connection_type_list:
        c = str(c)
        gamecodeexists = c.split(", ", 3)[1]
        status = c.split(", ", 3)[2]
        isStarted = c.split(", ", 3)[3]
        if gamecodeexists == gamecode and status.startswith("Created") and isStarted == "Started":
            print(c)
            i += 1
    return i


def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx

# Update client name display when a new client connects OR
# When a connected client disconnects
def insert_client_data_to_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c + "\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()