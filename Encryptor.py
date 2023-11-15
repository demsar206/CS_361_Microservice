from tkinter import *
import socket
import threading
from cryptography.fernet import Fernet
import json


# Create a socket for my partner's requests
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)

server.bind(server_address)
server.listen(5)


def listen_for_messages(partner_socket):
    """Listens for an incoming message, encrypts it, and sends it back out"""

    while True:
        partner_socket, address = server.accept()
        message = partner_socket.recv(1024).decode('utf-8')
        message_py = json.loads(message)
        e_message = fernet.encrypt(message_py)
        e_message_json = json.dumps(e_message)
        partner_socket.send(e_message_json.encode())

# Start the message listening thread
message_thread = threading.Thread(target=listen_for_messages, args=(server,), daemon=True)
message_thread.start()

# Generate an encryption key
key = Fernet.generate_key()
fernet = Fernet(key)


def clear():
    """Clears text from the text box"""
    my_text.delete(1.0, END)

def encrypt_text():
    """Encrypts a text"""

    text_to_encrypt = my_text.get(1.0, END)
    encrypted_text = fernet.encrypt(text_to_encrypt.encode())
    clear()
    my_text.insert(END, encrypted_text)

def decrypt_text():
    """Decrypts a text"""
    # Retrieve the text from the Text widget
    text_to_decrypt = my_text.get(1.0, END)

    try:

        decrypted_text = fernet.decrypt(text_to_decrypt.encode()).decode()
        clear()
        my_text.insert(END, decrypted_text)

    except Exception as e:
        print("Decryption error:", e)

def get_text():
    """Gets a text from my partner's microservice"""

    try:
        user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user_socket.connect(('localhost', 12345))

        request = "GET_TEXT"
        json_request = json.dumps(request)
        user_socket.send(json_request.encode())


        response = user_socket.recv(1024).decode()
        response_python = json.loads(response)

        my_text.insert(END, response_python)

        user_socket.close()

    except Exception as e:
        print("Error:", e)

def choice(option):
    """Clears the text box if popup option is Yes"""

    popup.destroy()
    if option == "Yes":
        clear()

def warning():
    """Create a warning pop-up for the clear button"""

    global popup
    popup = Toplevel(root)
    popup.title("warning")
    popup.geometry("250x150")
    popup.config(bg="red")

    warning_label = Label(popup, text= "You are about to clear the screen. Proceed?", width=50)
    warning_label.pack(pady=10)
    warning_frame = Frame(popup)
    warning_frame.pack(pady=5)
    yes = Button(warning_frame, text="Yes", command = lambda: choice("Yes"), bg="lightgrey")
    yes.grid(row= 0, column=1)
    yes = Button(warning_frame, text="No", command = lambda: choice("No"), bg = "lightgrey")
    yes.grid(row=0, column=2)

def about():
    global popup
    popup = Toplevel(root)
    popup.title("About")
    popup.geometry("1000x500")

    about_label = Label(popup, text="Click OK to close this window:")
    about_label.pack(pady=10)

    about_text = Text(popup, height=10, width=50,  wrap="word")
    about_text.insert('1.0',
                      "                    Information \n\n I’m making this program to learn about software development. "
                      "I’m hoping to take this program and build it out into a full messaging app at some point in the  "
                      "future. Thank you for using my program. If you have any questions or comments, you can reach me "
                      "at demsarw@oregonstate.edu.\n\n"
                      "                 Technical Details \n\n We use the Fernet class from the cryptography.fernet "
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


#tkinter GUI
root = Tk()
root.geometry("800x800")

instructions = Message(root, text = "Enter a message to encrypt or click 'Get Text' and you will be provided with a text." 
                                    "Click 'Encrypt' to encrypt your message and 'Decrypt' to decrypt your message.", width = 500)
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








