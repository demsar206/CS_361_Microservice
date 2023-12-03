from tkinter import *
import socket
import threading
from cryptography.fernet import Fernet
import json
import random


def handle_client(partner_socket):
    while True:
        try:
            message = partner_socket.recv(1024).decode('utf-8')
            if not message:
                break

            message_py = json.loads(message)
            e_message = fernet.encrypt(json.dumps(message_py).encode())
            partner_socket.send(e_message)

        except Exception as e:
            print("Error:", e)
            break

    partner_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server.bind(server_address)
    server.listen(5)

    while True:
        partner_socket, address = server.accept()
        print("Connected to:", address)

        handle_client_thread = threading.Thread(target=handle_client, args=(partner_socket,))
        handle_client_thread.start()

# clears text in GUI
def clear():
    my_text.delete(1.0, END)

# Encrypts text
def encrypt_text():
    text_to_encrypt = my_text.get(1.0, END)
    encrypted_text = fernet.encrypt(text_to_encrypt.encode())
    clear()
    my_text.insert(END, encrypted_text)

# Decrypts text
def decrypt_text():
    text_to_decrypt = my_text.get(1.0, END)

    try:
        decrypted_text = fernet.decrypt(text_to_decrypt.encode()).decode()
        clear()
        my_text.insert(END, decrypted_text)
    except Exception as e:
        print("Decryption error:", e)

# Gets text from partner's microservice
def get_text():
    cities = [
        {'city': 'Cleveland', 'state': 'Ohio'},
        {'city': 'New York City', 'state': 'New York'},
        {'city': 'Los Angeles', 'state': 'California'},
        {'city': 'Chicago', 'state': 'Illinois'},
        {'city': 'Houston', 'state': 'Texas'},
        {'city': 'Philadelphia', 'state': 'Pennsylvania'},
        {'city': 'Phoenix', 'state': 'Arizona'},
        {'city': 'San Antonio', 'state': 'Texas'},
        {'city': 'San Diego', 'state': 'California'},
        {'city': 'Dallas', 'state': 'Texas'},
        {'city': 'San Jose', 'state': 'California'},
        {'city': 'Austin', 'state': 'Texas'},
        {'city': 'Jacksonville', 'state': 'Florida'},
        {'city': 'San Francisco', 'state': 'California'},
        {'city': 'Indianapolis', 'state': 'Indiana'},
        {'city': 'Seattle', 'state': 'Washington'},
        {'city': 'Denver', 'state': 'Colorado'},
        {'city': 'Washington', 'state': 'D.C.'},
        {'city': 'Boston', 'state': 'Massachusetts'},
        {'city': 'Nashville', 'state': 'Tennessee'},
        {'city': 'Baltimore', 'state': 'Maryland'},
    ]

    random_city_state = random.choice(cities)

    try:
        user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user_socket.connect(('localhost', 55750))

        request = {
            'request-type': 'current-conditions',
            'city': random_city_state['city'],
            'state': random_city_state['state']
        }


        json_request = json.dumps(request)
        user_socket.send(json_request.encode('utf-8'))

        response = user_socket.recv(1024).decode('utf-8')
        response_python = json.loads(response)

        my_text.insert(END, response_python)

        user_socket.close()

    except Exception as e:
        print("Error:", e)

# User choice for warning box
def choice(option):
    popup.destroy()
    if option == "Yes":
        clear()

# Displays warning for clear button
def warning():
    global popup
    popup = Toplevel(root)
    popup.title("warning")
    popup.geometry("250x150")
    popup.config(bg="red")

    warning_label = Label(popup, text="You are about to clear the screen. Proceed?", width=50)
    warning_label.pack(pady=10)
    warning_frame = Frame(popup)
    warning_frame.pack(pady=5)
    yes = Button(warning_frame, text="Yes", command=lambda: choice("Yes"), bg="lightgrey")
    yes.grid(row=0, column=1)
    no = Button(warning_frame, text="No", command=lambda: choice("No"), bg="lightgrey")
    no.grid(row=0, column=2)

# 'About' window
def about():
    global popup
    popup = Toplevel(root)
    popup.title("About")
    popup.geometry("1000x500")

    about_label = Label(popup, text="Click OK to close this window:")
    about_label.pack(pady=10)

    about_text = Text(popup, height=10, width=50, wrap="word")
    about_text.insert('1.0',
                      "Information \n\n I’m making this program to learn about software development. "
                      "I’m hoping to take this program and build it out into a full messaging app at some point in the  "
                      "future. Thank you for using my program. If you have any questions or comments, you can reach me "
                      "at demsarw@oregonstate.edu.\n\n"
                      "Technical Details \n\n We use the Fernet class from the cryptography.fernet "
                      "module in Python. First, we generate a random encryption key with fernet.generate_key(). Next, we "
                      "initialize the key to encrypt or decrypt the message. The Get Text key sends a request to a "
                      "microservice using Python socket and posts the text to the text window. A separate port "
                      "listens for requests from another microservice to encrypt and send back data. Threading "
                      "is used to run these two functions at the same time.")
    about_text.config(state='disabled')
    about_text.pack(pady=5)

    button_frame = Frame(popup)
    button_frame.pack()

    ok_button = Button(button_frame, text="OK", command=popup.destroy)
    ok_button.pack()

    about_text.config(state='disabled')
    about_text.pack(pady=5)

    button_frame = Frame(popup)
    button_frame.pack()


# Initialize encryption key
key = Fernet.generate_key()
fernet = Fernet(key)

# Start server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Run GUI in the main thread
root = Tk()
root.geometry("800x800")

instructions = Message(root, text="Enter a message to encrypt or click 'Get Text' and you will be provided with a text."
                                  "Click 'Encrypt' to encrypt your message and 'Decrypt' to decrypt your message.",
                       width=500)
instructions.pack()

about_button = Button(root, text="About", command=about)
about_button.pack(pady=10)

my_text = Text(root, width=60, height=40)
my_text.pack(pady=5)

button_box = Frame(root)
button_box.pack()

clear_button = Button(button_box, text="Clear", command=warning)
encrypt_button = Button(button_box, text="Encrypt", command=encrypt_text)
decrypt_button = Button(button_box, text="Decrypt", command=decrypt_text)
get_text_button = Button(button_box, text="Get Text", command=get_text)

clear_button.grid(row=0, column=0)
encrypt_button.grid(row=0, column=1)
decrypt_button.grid(row=0, column=2)
get_text_button.grid(row=0, column=3)

root.mainloop()
