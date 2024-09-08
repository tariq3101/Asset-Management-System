import sqlite3
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from Addtional_features import MyCombobox, MyEntry
from PIL import Image, ImageTk
import datetime
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# USER MENU
BACKGROUND_COLOR = "#f7f7f7"
FORM_BG_COLOR = "#FFFFFF"
BG = "#ffffff"
FG = "#000000"
# NAV_COLOR = '#ffffff'
# NAV_TEXT_COLOR = '#000000'
NAV_COLOR = '#1b1a1a'
NAV_TEXT_COLOR = '#ffffff'


class User():
    def __init__(self, main_win):
        self.main_window = main_win

    def user_mainmenu(self):
        self.mainframe = Canvas(self.main_window, bg=NAV_COLOR, highlightthickness=1)
        self.mainframe.grid(column=0, row=1, columnspan=1, rowspan=15)

        image1 = Image.open("images/items.png")
        resize_image4 = image1.resize((50, 50))
        self.mi1 = ImageTk.PhotoImage(resize_image4)
        self.accounts = Button(self.mainframe, image=self.mi1, border=0, bg=NAV_COLOR, command=self.builditemtable)
        self.accounts.grid(column=0, row=1, padx=16, pady=(20, 0))
        self.label1 = Label(self.mainframe, text="Items", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
        self.label1.grid(column=0, row=2, pady=(5, 10))

        image2 = Image.open("images/invoice.png")
        resize_image2 = image2.resize((50, 50))
        self.mi2 = ImageTk.PhotoImage(resize_image2)
        self.sales = Button(self.mainframe, image=self.mi2, border=0, bg=NAV_COLOR,
                            command=self.make_invoice)
        self.sales.grid(column=0, row=3, pady=(10, 0))
        self.label2 = Label(self.mainframe, text="Invoice", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
        self.label2.grid(column=0, row=4, pady=(5, 10))

        image3 = Image.open("images/change user.png")
        resize_image3 = image3.resize((50, 50))
        self.mi3 = ImageTk.PhotoImage(resize_image3)
        self.changeuser = Button(self.mainframe, image=self.mi3, border=0, bg=NAV_COLOR)
        self.changeuser.grid(column=0, row=5, pady=(10, 0))
        self.label3 = Label(self.mainframe, text="Sign Out", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
        self.label3.grid(column=0, row=6, pady=(5, 15))

        image4 = Image.open("images/quit.png")
        resize_image4 = image4.resize((50, 50))
        self.mi4 = ImageTk.PhotoImage(resize_image4)
        self.logout = Button(self.mainframe, image=self.mi4, border=0, bg=NAV_COLOR)
        self.logout.grid(column=0, row=9, pady=(10, 0))
        self.label4 = Label(self.mainframe, text="Quit", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
        self.label4.grid(column=0, row=10, pady=(5, 218))

        image7 = Image.open("images/fine.png")
        resize_image7 = image7.resize((50, 50))
        self.mi7 = ImageTk.PhotoImage(resize_image7)
        self.fineimg = Button(self.mainframe, image=self.mi7, border=0, bg=NAV_COLOR, command=self.fine1)
        self.fineimg.grid(column=0, row=7, pady=(10, 0))
        self.label7 = Label(self.mainframe, text="Fine", bg=NAV_COLOR, fg=NAV_TEXT_COLOR)
        self.label7.grid(column=0, row=8, pady=(5, 20))


        self.tableframe1 = Frame(self.main_window, width=150, height=600, bg="#ffffff")
        self.tableframe1.place(x=1370, y=180, anchor=NE)
        self.tableframe1info = self.tableframe1.place_info()

        self.tableframe = Frame(self.main_window, width=350, height=700, bg="#ffffff")
        self.tableframe.place(x=1070, y=230, anchor=NE)
        self.tableframeinfo = self.tableframe.place_info()

        self.entryframe = Frame(self.main_window, width=440, height=350, bg="#ffffff")
        self.entryframe.place(x=790, y=410)
        self.entryframeinfo = self.entryframe.place_info()

        self.entryframe1 = Frame(self.main_window, width=500, height=350, bg="#ffffff")
        self.entryframe1.place(x=230, y=410)
        self.entryframe1info = self.entryframe1.place_info()

        self.searchframe = Frame(self.main_window, width=720, height=70, bg="#B0C4FC")
        self.searchframe.place(x=575, y=300)
        self.searchframeinfo = self.searchframe.place_info()

        self.searchbut = Button(self.searchframe, text="Search Description", font="roboto 14", bg="#FFFFFF", bd=5, command=self.searchprod)
        self.searchbut.place(x=0, y=20, height=40)

        self.searchvar = StringVar()
        self.searchentry = MyEntry(self.searchframe, textvariable=self.searchvar, font="roboto 14", width=25,bg="#FFFFFF")
        self.searchentry.place(x=210, y=20, height=40)

        self.resetbut = Button(self.searchframe, text="Reset", font="roboto 14", bd=5, width=8, bg="#FFFFFF", command=self.resetprodtabel)
        self.resetbut.place(x=510, y=18, height=40)

        self.tableframe2 = Frame(self.main_window, width=350, height=700, bg="#ffffff")
        self.tableframe2.place(x=370, y=230, anchor=NE)
        self.tableframeinfo = self.tableframe.place_info()

        
        self.make_invoice()

    def active(self, label):
        self.label1.config(fg='#ffffff')
        self.label2.config(fg="#ffffff")
        self.label3.config(fg="#ffffff")
        self.label4.config(fg="#ffffff")
        label.config(fg='#00ffff')

    def builditemtable(self):
        self.entryframe.place_forget()
        self.entryframe1.place_forget()
        self.tableframe2.place_forget()
        self.searchframe.place_forget()
        self.tableframe.place(self.tableframeinfo)
        self.tableframe1.place_forget()
        self.active(self.label1)
        scrollbarx = Scrollbar(self.tableframe, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe, columns=("Product ID", "Product Name", "Description", "Category",
                                                           'Price', 'Stocks'), selectmode="extended", height=18,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.tree.column('#6', stretch=NO, minwidth=0, width=100)
        self.tree.heading('Product ID', text="Product ID", anchor=W)
        self.tree.heading('Product Name', text="Product Name", anchor=W)
        self.tree.heading('Description', text="Description", anchor=W)
        self.tree.heading('Category', text="Category", anchor=W)
        self.tree.heading('Price', text="Price", anchor=W)
        self.tree.heading('Stocks', text="Stocks", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getproducts()

    def getproducts(self):
        self.cur.execute("select * from products")
        productlist = self.cur.fetchall()
        for i in productlist:
            self.tree.insert('', 'end', values=i)

    def make_invoice(self):
        self.tableframe.place_forget()
        self.tableframe2.place_forget()
        self.searchframe.place_forget()
        self.entryframe.place(self.entryframeinfo)
        self.entryframe1.place(self.entryframe1info)
        self.tableframe1.place(self.tableframe1info)
        self.active(self.label2)
        scrollbarx = Scrollbar(self.tableframe1, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe1, columns=("Transaction ID", "Product ID", "Product Name",
                                                            'Quantity', 'Price', 'Date', 'Time', 'Due Date','User'), selectmode="browse",
                                 height=6,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=140)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=170)
        self.tree.column('#4', stretch=NO, minwidth=0, width=130)
        self.tree.column('#5', stretch=NO, minwidth=0, width=130)
        self.tree.column('#6', stretch=NO, minwidth=0, width=130)
        self.tree.column('#7', stretch=NO, minwidth=0, width=130)
        self.tree.column('#8', stretch=NO, minwidth=0, width=130)
        self.tree.column('#9', stretch=NO, minwidth=0, width=130)
        self.tree.heading('Transaction ID', text="Transaction ID", anchor=W)
        self.tree.heading('Product ID', text="Product ID", anchor=W)
        self.tree.heading('Product Name', text="Product Name", anchor=W)
        self.tree.heading('Quantity', text="Quantity", anchor=W)
        self.tree.heading('Price', text="Price", anchor=W)
        self.tree.heading('Date', text="Date", anchor=W)
        self.tree.heading('Time', text="Time", anchor=W)
        self.tree.heading('Due Date', text="Due Date", anchor=W)
        self.tree.heading('User', text="User", anchor=W)

        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.tree.bind("<<TreeviewSelect>>", self.clicktranstable)
        self.user_input()

    def user_input(self):
        self.cur.execute('select max(trans_id) from sales')
        li = self.cur.fetchall()
        if li[0][0] != None:
            self.transid = li[0][0] + 1
        else:
            self.transid = 100
        self.qty = StringVar(value=1)
        self.additem = StringVar()
        self.total = IntVar(value=0)
        Button(self.entryframe, text="Proceed", command=self.transtableadd, bd=10, width=8, height=7, bg="#FFFFFF",
               font="roboto 10").place(x=0, y=30)
        Button(self.entryframe, text="Add to cart", command=self.addtotrans, bd=10, width=10, height=3, bg="#FFFFFF",
               font="roboto 10").place(x=100, y=80)
        Button(self.entryframe, text="Remove", command=self.removecart, bd=10, width=10, height=3, bg="#FFFFFF",
               font="roboto 10").place(x=210, y=80)
        
        Label(self.entryframe, text="Search", font="roboto 12 bold", bg="#ffffff").place(x=100, y=0)
        entercart = MyCombobox(self.entryframe, width=20, textvariable=self.additem, font="roboto 12")
        entercart.place(x=100, y=30, height=30)

        Label(self.entryframe, text="Quantity", font="roboto 12 bold", bg="#ffffff").place(x=318, y=0)
        cartqty = Entry(self.entryframe, textvariable=self.qty, width=9, bg="#ffffff", font="roboto 12")
        cartqty.place(x=320, y=30, height=30)

        Label(self.entryframe, text="Due Date", font="roboto 12 bold", bg="#ffffff").place(x=318, y=70)
        self.rental_duration = ttk.Combobox(self.entryframe, width=15, values=["1 month", "2 months", "3 months", "4 months", "5 months"])
        self.rental_duration.place(x=320, y=94, height=30)

        carttotal = Entry(self.entryframe, textvariable=self.total, width=20, state='readonly', bg="#ffffff",
                          font="roboto 12")
        carttotal.place(x=130, y=185, height=60)
        Label(self.entryframe, text="Amount Due", font="roboto 14 bold", bg="#ffffff").place(x=0, y=205)
        self.cur.execute("select max(invoice) from sales")
        self.invoice = self.cur.fetchall()
        self.invoice = self.invoice[0][0] + 1
        Label(self.tableframe1, text="Invoice No. " + str(self.invoice), font="roboto 14 bold", bg="#ffffff").grid(
            row=0, column=0)
        self.cur.execute("select product_name,product_price from products")
        li = self.cur.fetchall()
        self.inventory = []
        self.desc_price = dict()
        for i in range(0, len(li)):
            if self.inventory.count(li[i][0]) == 0:
                self.inventory.append(li[i][0])
            self.desc_price[li[i][0]] = li[i][1]
        entercart.set_completion_list(self.inventory)
        li = ['Product Id', 'Product Name', 'Price', 'Left Stock']
        va = 0
        for i in range(0, 4):
            Label(self.entryframe1, text=li[i], font="roboto 14 bold", bg="#FFFFFF").place(x=0, y=va)
            va += 65
        self.cartitemid = StringVar()
        self.cartitem = StringVar()
        self.cartitemprice = StringVar()
        self.cartitemstock = StringVar()
        Entry(self.entryframe1, textvariable=self.cartitemid, font="roboto 14", bg="#FFFFFF", width=25,
              state='readonly').place(x=162, y=0, height=40)
        Entry(self.entryframe1, textvariable=self.cartitem, font="roboto 14", bg="#FFFFFF", width=25,
              state='readonly').place(x=162, y=65, height=40)
        Entry(self.entryframe1, textvariable=self.cartitemprice, font="roboto 14", bg="#FFFFFF", width=25,
              state='readonly').place(x=162, y=65 * 2, height=40)
        Entry(self.entryframe1, textvariable=self.cartitemstock, font="roboto 14", bg="#FFFFFF", width=25,
              state='readonly').place(x=162, y=65 * 3, height=40)
        self.id_qty = dict()
        self.cur.execute("select product_id from products")
        list_ = self.cur.fetchall()
        for i in range(0, len(list_)):
            self.id_qty[list_[i][0]] = 0

    def addtotrans(self):
        if len(self.additem.get()) == 0 or self.inventory.count(self.additem.get()) == 0:
            messagebox.showerror("Error", "Product Not Found!")
            return
        else:
            if not self.qty.get().isdigit():
                messagebox.showerror('Error', 'Invalid quantity!')
                return
            if int(self.qty.get()) <= 0:
                messagebox.showerror('Error', 'Invalid quantity!')
                return
            if len(self.rental_duration['values']) == 0:
                messagebox.showerror('Error', 'Please provide due date!')
            self.cur.execute("select product_id,product_name from products where product_name = ? ",
                             (self.additem.get(),))
            row = self.cur.fetchall()
            row = [list(row[0])]
            row[0].insert(0, self.transid)
            self.transid += 1
            row[0].append(int(self.qty.get()))
            row[0].append((int(self.qty.get()) * self.desc_price[self.additem.get()]))
            x = str(datetime.datetime.now().strftime("%d-%m-%y"))
            row[0].append(x)
            x = datetime.datetime.now()
            x = str(x.hour) + ' : ' + str(x.minute) + ' : ' + str(x.second)
            row[0].append(x)
            try: 
                due_date = datetime.datetime.now() + datetime.timedelta(days=30 * int(self.rental_duration.get().split()[0]))
                due_date_str = due_date.strftime("%Y-%m-%d")
                row[0].append(due_date_str)
            except IndexError:
                messagebox.showerror('Error', 'Please enter return date!')
                return
            username = (self.username.get()).capitalize()
            row[0].append(username)

            row = [tuple(row[0])]
            self.cartitemid.set(row[0][1])
            self.cartitemprice.set(self.desc_price[self.additem.get()])
            self.cartitem.set(row[0][2])
            self.cur.execute("select stocks from products where product_id=?", (row[0][1],))
            li = self.cur.fetchall()
            if (li[0][0] - self.id_qty[row[0][1]]) - int(self.qty.get()) < 0:
                if li[0][0] != 0:
                    messagebox.showerror('Error', 'Product with this quantity not available!')
                else:
                    messagebox.showerror('Error', 'Product out of stock!')
                return
            self.id_qty[row[0][1]] += int(self.qty.get())
            self.cartitemstock.set(li[0][0] - self.id_qty[row[0][1]])
            for data in row:
                self.tree.insert('', 'end', values=data)
            self.total.set(self.total.get() + (int(self.qty.get()) * self.desc_price[self.additem.get()]))
            self.qty.set('1')
            self.additem.set('')

    def transtableadd(self):
        x = self.tree.get_children()
        if len(x) == 0:
            messagebox.showerror('Error', 'Empty cart!')
            return
        if not messagebox.askyesno('Alert!', 'Do you want to proceed?'):
            return
        a = []

        self.cur.execute("select max(invoice) from sales")
        self.invoice = self.cur.fetchall()
        self.invoice = self.invoice[0][0] + 1
        for i in x:
            list_ = self.tree.item(i)
            a.append(list_['values'])
        for i in a:
            due_date = datetime.datetime.now() + datetime.timedelta(days=30 * int(self.rental_duration.get().split()[0]))
            due_date_str = due_date.strftime("%Y-%m-%d")
            i.append(due_date_str)
            s = (str(i[5])).split('-')
            i[5] = s[2] + "-" + s[1] + "-" + s[0]
            
            # self.cur.execute("insert into sales values (?,?,?,?,?,?)",
            #                  (int(i[0]), int(self.invoice), int(i[1]), int(i[3]), i[5], i[6]))
            self.cur.execute("insert into sales (Trans_id, invoice, Product_id, Quantity, Date, Time, due_date, user) values (?,?,?,?,?,?,?,?)",
                 (int(i[0]), int(self.invoice), int(i[1]), int(i[3]), i[5], i[6], i[7], i[8]))

            self.cur.execute("select stocks from products where product_id=?", (int(i[1]),))
            list_ = self.cur.fetchall()
            self.cur.execute("update products set stocks=? where product_id=?",
                             (list_[0][0] - self.id_qty[str(i[1])], int(i[1])))
            self.base.commit()
        messagebox.showinfo('Success', 'Transaction Successful!')
        self.makeprint()
        self.tree.delete(*self.tree.get_children())
        self.cartitemstock.set('')
        self.cartitem.set('')
        self.cartitemid.set('')
        self.cartitemprice.set('')
        self.total.set(0)
        self.additem.set('')
        self.qty.set('1')
        self.cur.execute("select product_id from products")
        list_ = self.cur.fetchall()
        for i in range(0, len(list_)):
            self.id_qty[list_[i][0]] = 0
        self.make_invoice()

    def removecart(self):
        remove = self.tree.selection()
        if len(remove) == 0:
            messagebox.showerror('Error', 'No cart selected')
            return
        if messagebox.askyesno('Alert!', 'Remove cart?'):
            x = self.tree.get_children()
            remove = remove[0]
            list_ = []
            fi = []
            for i in x:
                if i != remove:
                    list_.append(tuple((self.tree.item(i))['values']))
                else:
                    fi = ((self.tree.item(i))['values'])
            self.tree.delete(*self.tree.get_children())
            for i in list_:
                self.tree.insert('', 'end', values=i)
            self.cartitemstock.set('')
            self.cartitem.set('')
            self.cartitemid.set('')
            self.cartitemprice.set('')
            self.additem.set('')
            self.qty.set('1')
            self.id_qty[str(fi[1])] -= fi[3]
            self.total.set(self.total.get() - fi[4])
            return

    def makeprint(self):
        if messagebox.askyesno("Alert!", "Print this transaction?"):
            invoice_number = f"Invoice Number: {self.invoice}"

            data = []
            for child in self.tree.get_children():
                values = self.tree.item(child, 'values')
                data.append(values)

            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if filename:
                doc = SimpleDocTemplate(filename, pagesize=letter)
                elements = []

                style_sheet = getSampleStyleSheet()
                header_style = style_sheet['Heading1']
                header_style.alignment = 1  # Center alignment
                header_paragraph = Paragraph(invoice_number, header_style)
                elements.append(header_paragraph)

                table_data = [['Transaction ID', 'Product ID', 'Product Name', 'Quantity', 'Price', 'Date', 'Time', 'Due Date','User']]
                for item in data:
                    table_data.append(item)
                table = Table(table_data)

                style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])
                table.setStyle(style)
                elements.append(table)

                doc.build(elements)
                messagebox.showinfo("Success", "PDF generated successfully!")


    def clicktranstable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if len(li) == 7:
            self.cartitemid.set((li[1]))
            self.cartitem.set((li[2]))
            self.cur.execute("select product_price,stocks from products where product_id=?", (li[1],))
            li = self.cur.fetchall()
            self.cartitemprice.set(li[0][0])
            self.cartitemstock.set(li[0][1] - self.id_qty[self.cartitemid.get()])
    
    def fine1(self):
        self.tableframe.place_forget()
        self.tableframe1.place_forget()
        self.entryframe.place_forget()
        self.entryframe1.place_forget()

        today_date = datetime.datetime.now().date()

        self.cur.execute("SELECT * FROM sales")
        sales = self.cur.fetchall()

        for sale in sales:
            if sale[6] is not None:
                sale_date = datetime.datetime.strptime(sale[6], "%Y-%m-%d").date()
                # print(sale_date)
                days_diff = (today_date - sale_date).days
                # print(days_diff)
                if days_diff > 0:
                    fine_amount = days_diff * 3  

                    self.cur.execute("UPDATE sales SET fine = ? WHERE Trans_id = ?", (fine_amount, sale[0]))
                    self.base.commit()
                # else:
                #     messagebox.showerror('Error','Due date is missing for a sale record.')
                #     return
        # self.buildsalestable()
        self.tableframe2.place(x=875, y=255, anchor=NE)
        self.tree.delete(*self.tree.get_children())
        self.tree.grid_remove()
        self.tree.destroy()
        self.active(self.label2)
        scrollbarx = Scrollbar(self.tableframe2, orient=HORIZONTAL)
        scrollbary = Scrollbar(self.tableframe2, orient=VERTICAL)
        self.tree = ttk.Treeview(self.tableframe2,
                                 columns=('Product', 'Date', 'Due Date','Fine'),
                                 selectmode="browse", height=16,
                                 yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=140)
        self.tree.column('#2', stretch=NO, minwidth=0, width=140)
        self.tree.heading('Product', text="Product", anchor=W)
        self.tree.heading('Date', text="Date", anchor=W)
        self.tree.heading('Due Date', text='Due Date', anchor=W)
        self.tree.heading('Fine', text='Fine', anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")

        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)

        # self.cur.execute("INSERT INTO fine (Date, due_date, user, fine) SELECT Date, due_date, user, fine FROM sales")
        self.getsales1()
        self.totalsales = Label(self.tableframe2, text="Total Sales", font="roboto 14 bold").place(x=0, y=400)
        
    def getsales1(self):
        username = (self.username.get()).capitalize()
        self.cur.execute("SELECT * FROM sales where user = ? ",(username,))
        saleslist = self.cur.fetchall()
        for i in range(len(saleslist)):
            saleslist[i] = list(saleslist[i])
            s = str(saleslist[i][4]).split('-')
            saleslist[i][4] = f"{s[2]} - {s[1]} - {s[0]}"
            self.cur.execute("SELECT product_name FROM products WHERE product_id = ?", (saleslist[i][2],))
            product_name = self.cur.fetchone()[0]  
            saleslist[i][0] = product_name 
            saleslist[i] = [saleslist[i][0],saleslist[i][4],saleslist[i][6],saleslist[i][8]] 
            saleslist[i] = tuple(saleslist[i])
        for i in saleslist:
            self.tree.insert('', 'end', values=i)


   