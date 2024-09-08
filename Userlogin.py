import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


# LOGIN CLASS
class Login:

    def __init__(self):
        self.loginw = Tk()
        self.loginw.title("Login")
        width = 550
        height = 600
        screen_width = self.loginw.winfo_screenwidth()
        screen_height = self.loginw.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.loginw.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.loginw.resizable(0, 0)
        self.loginw.protocol('WM_DELETE_WINDOW', self.__login_del__)
        self.loginw.config(bg="#4267b2")
        image = Image.open("images/loginbg.png")
        resize_image = image.resize((550, 600))
        self.img = ImageTk.PhotoImage(resize_image)

        self.bgimage = Label(
            self.loginw,
            image=self.img
        )
        self.bgimage.place(x=-2, y=-2)

        self.logintable()
        self.username = StringVar(value="Username")
        self.password = StringVar(value="Password")
        self.obj()

    def __login_del__(self):
        if messagebox.askyesno("Quit", " Leave application?"):
            self.loginw.destroy()
            exit(0)  # FORCE SYSTEM TO EXIT

    # LOGIN TABLE
    def logintable(self):
        self.base = sqlite3.connect("login.db")
        self.cur = self.base.cursor()
        self.cur.execute(
            "CREATE TABLE if not exists users (name varchar (20), phone_no number, gender varchar(10), username varchar (20),password varchar (20) NOT NULL,account_type varchar ( 10 ) NOT NULL,PRIMARY KEY(username));")

    # WIDGET FUNCTION
    def obj(self):
        self.loginframe = Canvas(self.loginw, bg="#e4d9ff", height=450, width=350)
        self.loginw.bind('<Return>', self.checkuser)
        self.loginframe.place(x=100, y=75)

        #login label
        self.toplabel = Label(self.loginframe, fg="black", bg="#e4d9ff", anchor="center", text="Login",font=('yu gothic ui' ,28,'bold'))
        self.loginframe.configure(highlightthickness=0, bd=0)
        self.toplabel.place(x=115, y=30)

        #Username label and textfield
        self.userlabel = Label(self.loginframe, height=2, fg="black",bg="#e4d9ff", anchor="center", text="Username:", font=('yu gothic ui' ,13,'bold'))
        self.userlabel.place(x=10, y=145)
        self.us_line=Canvas(self.loginframe,width=200,height=2,bg='#bdb9b1',highlightthickness=0)
        self.us_line.place(x=111,y=190)
        self.us = Entry(self.loginframe, width=20,bg="#e4d9ff", textvariable=self.username, border=0, justify='center', font=('yu gothic ui' ,13,'bold'))
        self.us.place(x=110, y=150, height=40, width=200)
        self.loginframe.configure(highlightthickness=0, bd=0)

        #Password label and textfield
        self.userlabel = Label(self.loginframe, height=2,fg="black",bg="#e4d9ff", anchor="center", text="Password:",font=('yu gothic ui' ,13,'bold'))
        self.userlabel.place(x=10, y=210)
        self.pa = Entry(self.loginframe, width=20,bg="#e4d9ff", textvariable=self.password, border=0, justify='center',font=('yu gothic ui' ,13,'bold'))
        self.pa.place(x=110, y=215, height=40,width=200)
        self.pa_line=Canvas(self.loginframe,width=200,height=2,bg='#bdb9b1',highlightthickness=0)
        self.pa_line.place(x=111,y=250)
        self.loginframe.configure(highlightthickness=0, bd=0)

        self.us.bind('<Button-1>', self.onclick)
        self.pa.bind('<Button-1>', self.onclick1)
        self.signin = Button(self.loginframe, width=20, text="Sign in", bg="#cbc5ea", fg="black",command=self.checkuser,font=('yu gothic ui' ,14,'bold'))
        self.signin.place(x=55, y=290)

    # CHECK USER IN DATABASE
    def checkuser(self, event=0):
        s = self.username.get()
        s1 = self.password.get()
        s = s.upper()
        s1 = s1.upper()
        self.cur.execute("select * from users where username=? and password=? ", (s, s1))
        list_ = self.cur.fetchall()
        if len(list_) > 0:
            self.success()
        else:
            self.fail()

    # LOGIN SUCCESS
    def success(self):
        # messagebox.showinfo("Success","Login successful")
        self.loginw.quit()

    # LOGIN FAILURE
    def fail(self):
        messagebox.showerror("Error", "The username or password is incorrect")

    # USER REGISTRATION && LOGIN->REGISTER
    def reguser(self):
        self.toplabel.config(text="Register")
        self.toplabel.place(x=80, y=25)
        self.username.set("Choose your username")
        self.password.set("Create a password")
        self.signin.config(text="Ok", command=self.insert)
        self.register = Button(self.loginframe, width=20, text="Back", bg="#9933ff", fg="white",
                               command=self.revert, font="Roboto 14")
        self.register.place(x=35, y=320)
        self.signin.config()
        self.signin.place(x=35, y=260)
        self.pa.config(show='')
        self.loginw.focus()
        self.loginw.bind('<Return>', self.insert)
        self.loginw.title('Register')

    # REGISTER USER TO DATABASE
    def insert(self, event=0):
        s = self.username.get()
        s1 = self.password.get()
        s = s.upper()
        s1 = s1.upper()
        self.cur.execute("select username from users where username = ?", (s,))
        list_ = self.cur.fetchall()
        if len(list_) > 0:
            messagebox.showerror("Error", "Username already exist")
            self.username.set('Choose your username')
            self.loginw.focus()
            return
        if (len(s) == 0 or len(s1) == 0 or len(s) > 20 or len(
                s1) > 20 or s1 == "CREATE A PASSWORD" or s == 'CHOOSE YOUR USERNAME'):
            messagebox.showerror("Error", "Invalid username or password")
            self.username.set('Choose your username')
            self.password.set('Create a password')
            self.pa.config(show='')
            self.loginw.focus()
            return
        else:
            self.cur.execute("insert into users values(?,?,?)", (s, s1, 'USER'))
            messagebox.showinfo("Success", "User registered")
            self.base.commit()
            self.revert()
            # ADD
            self.loginw.state('withdraw')
            self.tree.delete(*self.tree.get_children())
            self.getusers()

    # REGISTER->LOGIN
    def revert(self):
        self.toplabel.config(text="Login")
        self.toplabel.place(x=75, y=25)
        self.signin.config(text="Sign in", command=self.checkuser)
        self.register.config(text="Register", command=self.reguser)
        self.username.set('Username')
        self.password.set('Password')
        self.pa.config(show='')
        self.signin.config(state=NORMAL)
        self.loginw.focus()
        self.loginw.bind('<Return>', self.checkuser)
        # ADD
        self.signin.place(x=35, y=290)
        self.loginw.title('Login')
        self.loginw.state('withdraw')

    # ONCLICK EVENTS
    def onclick(self, event):
        if self.username.get() == "Username" or self.username.get() == "Choose your username":
            self.us.delete(0, "end")

    def onclick1(self, event):
        if self.password.get() == "Password" or self.password.get() == "Create a password":
            self.pa.delete(0, "end")
            self.pa.config(show="*")