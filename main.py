import customtkinter as ctk
import tkinter as tk

import json
import requests


ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("ChatGPT-Bot")
        self.geometry("700x650")
        self.initialize_gui()

    def send_message(self,event):
        self.box.configure(state= "normal")
        self.box.insert(tk.END,"User: " + self.user.get() + "\n"+ "\n")
        print(self.user.get())
        self.box.insert(tk.END,"Bot: " + self.answer_message(self.user.get()) + "\n"+ "\n")
        self.user.delete(0,tk.END)
        self.box.configure(state= "disabled")
        
    def answer_message(self,message):
        url = "https://api.theb.ai/v1/chat/completions"
        with open('dat.json') as f:
            data = json.load(f)
            api_key = data["API_KEY"]

        payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False
        })
        headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()["choices"][0]["message"]["content"]

    def initialize_gui(self):
        
        self.label_title = ctk.CTkLabel(self,text="Enter your message...",font=("Arial",28),)
        self.label_title.pack(side = tk.TOP,pady = 20)

        self.box = ctk.CTkTextbox(self,font = ("Calibri",22),width= 600,height= 400,fg_color="#242627",state = "disabled")
        self.box.pack(pady = 20)

        self.frame = ctk.CTkFrame(self,fg_color="#242627",width=600,height=100)
        self.frame.pack()

        self.user = ctk.CTkEntry(self.frame,width=450,height= 100,font = ("Arial",19),placeholder_text= "Make a question... and press enter",fg_color="#242627")
        self.user.pack(side = tk.LEFT)
        self.user.bind("<Return>",self.send_message)

        self.send = ctk.CTkButton(self.frame,width= 150,height=100,fg_color="#242627",text= "Send",command= lambda: self.send_message(None))
        self.send.pack(side = tk.RIGHT)

window = App()
window.configure(fg_color = "#181818")
window.mainloop()