from tkinter import *
import sys
import os
from datetime import date
from tkinter import messagebox
import webbrowser




class DashboardWindow:
    def __init__(self):
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=600, height=500, bg='blue')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("WELCOME | Dashboard | ADMINISTRATOR")
    
    def run1(self):
        os.system('python3 sms.py')

    def run2(self):
        today = date.today()
        getDate = today.strftime("%d/%m/%y")
        with open('/home/amir/Documents/face/doc/lastdate.txt','r') as f:
            f_content = f.read()
        
        if getDate == f_content:
            messagebox.showinfo("Alert!", "You Cann't Take Today's Attendance. Reset First!")
        else:
            os.system('python3 takeAtten.py')
    
    def run3(self):
        webbrowser.open_new(r'file:/home/amir/Documents/face/doc/python.xlsx')

    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        self.img = PhotoImage(file='/home/amir/Documents/face/forms/icon/C.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x = x + 80, y = y + 0)

        self.button = Button(self.frame, text="Student Management System", font='Courier 15 bold',
                             command=self.run1)
        self.button.place(x=x+20, y=y+150)

        self.button2 = Button(self.frame, text=" Take Today's Attendance ", font='Courier 15 bold',
                             command=self.run2)
        self.button2.place(x=x+20, y=y+200)

        self.button3 = Button(self.frame, text="   View Attendance   ", font='Courier 15 bold',
                             command=self.run3)
        self.button3.place(x=x+20, y=y+250)
        self.win.mainloop()