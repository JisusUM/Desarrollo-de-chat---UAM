from cProfile import label
from email.mime import image
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import *
import tkinter

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
AZUL = '#6495ED'
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


# Creando un objeto de enchufe
#AF_INET: vamos a usar direcciones IPv4
# SOCK_STREAM: estamos usando paquetes TCP para la comunicación
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
# intentar excepto bloquear
    try:
        
# Conectarse al servido
        client.connect((HOST, PORT))
        print("Conectado con éxito al servidor")
        add_message("[SERVER] Conectado con éxito al servidor")
    except:
        messagebox.showerror("No se puede conectar al servidor", f"No se puede conectar al servidor {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Nombre de usuario no válido", "El nombre de usuario no puede estar vacío")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("mensaje vacio", "El mensaje no puede estar vacío")

root = tk.Tk()
root.geometry("600x600")
#logo=tk.PhotoImage(file="code.gif")
"""image= image.subsample(3,3)
label=tk.Label(image=image)
label.pack()"""
root.title("Soporte Centro de informatica")
root.resizable(False, False)
logo=tk.PhotoImage(file="code.gif")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Nombre de usuario:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=4)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Unirse", font=BUTTON_FONT, bg=AZUL, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=AZUL, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Enviar", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)


message_box =scrolledtext.ScrolledText(middle_frame,font=SMALL_FONT,bg=None, fg=WHITE, width=67, height=26.5)
message_box=tk.Label(middle_frame,image=logo)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "El mensaje recibido del cliente está vacío.")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()