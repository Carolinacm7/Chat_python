import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        self.root = tk.Tk()
        self.root.title("Chat Cliente")
        
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind('<Return>', self.send_message)
        
        self.alias = simpledialog.askstring("Alias", "Elige un alias para el chat")
        self.client.send(self.alias.encode('utf-8'))
        
        threading.Thread(target=self.receive_messages).start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.exit_chat)
        self.root.mainloop()
    
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.update_chat_area(message)
            except:
                print("Conexión perdida con el servidor.")
                self.client.close()
                break
    
    def update_chat_area(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
    
    def send_message(self, event=None):
        message = self.entry.get()
        self.entry.delete(0, tk.END)
        if message:
            self.client.send(f"{self.alias}: {message}".encode('utf-8'))
    
    def exit_chat(self):
        self.client.close()
        self.root.destroy()

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 5000

if __name__ == "__main__":
    ChatClient(HOST, PORT)
