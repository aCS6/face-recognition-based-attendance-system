from tkinter import *
from tkinter import messagebox
import db.db
import dashboard


class LoginWindow:

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
        self.win.title("WELCOME | Login Window | ADMINISTRATOR")

    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        self.img = PhotoImage(file='/home/amir/Documents/face/forms/icon/B.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x = x + 80, y = y + 0)

        #now create a login form
        self.label = Label(self.frame, text="User Login")
        self.label.config(font=("Courier", 20, 'bold'))
        self.label.place(x=140, y = y + 150)

        self.emlabel = Label(self.frame, text="Enter Username")
        self.emlabel.config(font=("Courier", 12, 'bold'))
        self.emlabel.place(x=50, y= y + 230)

        self.user = Entry(self.frame, font='Courier 12')
        self.user.place(x=200, y= y + 230)

        self.pslabel = Label(self.frame, text="Enter Password")
        self.pslabel.config(font=("Courier", 12, 'bold'))
        self.pslabel.place(x=50, y=y+260)

        self.passs = Entry(self.frame,show='*', font='Courier 12')
        self.passs.place(x=200, y=y+260)

        self.button = Button(self.frame, text="Login", font='Courier 15 bold',
                             command=self.login)
        self.button.place(x=170, y=y+290)

        self.win.mainloop()

    def login(self):
        #get the data and store it into tuple (data)
        data = (
            self.user.get(),
            self.passs.get()
        )
        # validations
        if self.user.get() == "":
            messagebox.showinfo("Alert!","Enter Username First")
        elif self.passs.get() == "":
            messagebox.showinfo("Alert!", "Enter Password first")
        else:
            res = db.db.user_login(data)
            if res:
                messagebox.showinfo("Message", "Login Successfully")
                self.win.destroy()
                x = dashboard.DashboardWindow()
                x.add_frame()
            else:
                messagebox.showinfo("ALert!", "Wrong username/password")