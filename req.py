# Importing all required modules
import sqlite3

from tkinter import *
import tkinter.ttk as tk
import tkinter.messagebox as v
import tkinter.simpledialog as sd

# Connecting to Database
connect = sqlite3.connect('library.db')
cursor = connect.cursor()

connect.execute(
    'CREATE TABLE IF NOT EXISTS Library (BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL, AUTHOR_NAME TEXT, BK_STATUS TEXT, CARD_ID TEXT)'
)


# Functions i used
class Database:
    def __init__(self):
        pass
    def issuer_card(self):
        B_ID = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

        if not B_ID:
            v.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
        else:
            return B_ID


    def show_records(self):
        global connect, d
        global t

        t.delete(*t.get_children())

        curr = connect.execute('SELECT * FROM Library')
        data = curr.fetchall()

        for records in data:
            t.insert('', END, values=records)


    def empty_fields(self):
        global b_status, b_id, b_name, author_name, c_id

        b_status.set('Available')
        for i in ['b_id', 'b_name', 'author_name', 'c_id']:
            exec(f"{i}.set('')")
            b_id_entry.config(state='normal')
        try:
            t.selection_remove(t.choose()[0])
        except:
            pass


    def erase_and_show(self):
        self.empty_fields()
        self.show_records()


    def append_record(self):
        global connect
        global b_name, b_id, author_name, b_status

        if b_status.get() == 'Issued':
            c_id.set(self.issuer_card())
        else:
            c_id.set('N/A')

        surety = v.askyesno('Are you sure?',
                            'Are you sure this is the data you want to enter?\nPlease note that Book ID cannot be changed in the future')
        if surety:
            try:
                connect.execute(
                    'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                    (b_name.get(), b_id.get(), author_name.get(), b_status.get(), c_id.get()))
                connect.commit()

                self.erase_and_show()

                v.showinfo('Record added', 'The new record was successfully added to your database')
            except sqlite3.IntegrityError:
                v.showerror('Book ID is already in use!',
                            'The Book ID you are trying to enter is already in the database, please alter that book\'s record or check any discrepancies on your side')


    def display_record(self):
        global b_name, b_id, b_status, author_name, c_id
        global t

        if not t.focus():
            v.showerror('Select a row!',
                        'To view a record, you must select it in the table. Please do so before continuing.')
            return

        current_item_selected = t.focus()
        values_in_selected_item = t.item(current_item_selected)
        choose = values_in_selected_item['values']

        b_name.set(choose[0]);
        b_id.set(choose[1]);
        b_status.set(choose[3])
        author_name.set(choose[2])
        try:
            c_id.set(choose[4])
        except:
            c_id.set('')


    def upgrad_data(self):
        def update():
            global b_status, b_name, b_id, author_name, c_id
            global connect, t

            if b_status.get() == 'Issued':
                c_id.set(self.issuer_card())
            else:
                c_id.set('N/A')

            cursor.execute('UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? WHERE BK_ID=?',
                           (b_name.get(), b_status.get(), author_name.get(), c_id.get(), b_id.get()))
            connect.commit()

            self.erase_and_show()

            edit.destroy()
            b_id_entry.config(state='normal')
            clear.config(state='normal')

        self.display_record()

        b_id_entry.config(state='disable')
        clear.config(state='disable')

        edit = Button(lf, text='Update Record', font=btn_font, bg=button_bg, width=20, command=update)
        edit.place(x=50, y=375)


    def drop_info(self):
        if not t.choose():
            v.showerror('Does Not Exist!', 'Please select an item from the database')
            return

        current_item = t.focus()
        values = t.item(current_item)
        choose = values["values"]

        cursor.execute('DELETE FROM Library WHERE BK_ID=?', (choose[1],))
        connect.commit()

        t.delete(current_item)

        v.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        self.erase_and_show()


    def delete_info(self):
        if v.askyesno('Are you sure?',
                      'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
            t.delete(*t.get_children())

            cursor.execute('DELETE FROM Library')
            connect.commit()
        else:
            return


    def alter_availability(self):
        global c_id, t, connect

        if not t.choose():
            v.showerror('Error!', 'Please select a book from the database')
            return

        current_item = t.focus()
        values = t.item(current_item)
        BK_id = values['values'][1]
        BK_status = values["values"][3]

        if BK_status == 'Issued':
            surety = v.askyesno('Is return confirmed?', 'Has the book been returned to you?')
            if surety:
                cursor.execute('UPDATE Library SET b_status=?, c_id=? WHERE b_id=?', ('Available', 'N/A', BK_id))
                connect.commit()
            else:
                v.showinfo(
                    'Cannot be returned', 'The book status cannot be set to Available unless it has been returned')
        else:
            cursor.execute('UPDATE Library SET b_status=?, c_id=? where b_id=?', ('Issued', self.issuer_card(), BK_id))
            connect.commit()

        self.erase_and_show()

databasefunctions=Database()
lfc = 'royalblue'  # Left Frame Background Color
rfc = 'DeepSkyBlue'  # Right Top Frame Background Color
rf_bg = 'DarkGray'  # Right Bottom Frame Background Color
button_bg = 'steelblue'  # Background color for Head Labels and Buttons

label_font = ('Calibri', 14)  # Font for all labels
entry_font = ('Times New Roman', 13)  # Font for all Entry widgets
btn_font = ('Batang', 13)

# Initializing the main GUI window
root = Tk()
root.title('Python Project Library Management System')
root.geometry('1060x600')
root.resizable(0, 0)

Label(root, text='LIBRARY MANAGEMENT SYSTEM BY SOWMYA NADIPINENI', font=("calibri", 15, 'bold'), bg=button_bg,
      fg='black').pack(side=TOP, fill=X)

b_status = StringVar()
b_name = StringVar()
b_id = StringVar()
author_name = StringVar()
c_id = StringVar()

# Frames i am using
lf = Frame(root, bg=lfc)
lf.place(x=0, y=30, relwidth=0.3, relheight=0.96)

rt = Frame(root, bg=rfc)
rt.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

# Left Frame
Label(lf, text='Book Name', bg=lfc, font=label_font).place(x=98, y=25)
Entry(lf, width=25, font=entry_font, text=b_name).place(x=45, y=55)

Label(lf, text='BookID', bg=lfc, font=label_font).place(x=110, y=105)
b_id_entry = Entry(lf, width=25, font=entry_font, text=b_id)
b_id_entry.place(x=45, y=135)

Label(lf, text='Author Name', bg=lfc, font=label_font).place(x=90, y=185)
Entry(lf, width=25, font=entry_font, text=author_name).place(x=45, y=215)

Label(lf, text='Status of the Book', bg=lfc, font=label_font).place(x=75, y=265)
dd = OptionMenu(lf, b_status, *['Available', 'Issued', 'only few left'])
dd.configure(font=entry_font, width=12)
dd.place(x=75, y=300)

submit = Button(lf, text='Add new record', font=btn_font, bg=button_bg, width=20, command=databasefunctions.append_record)
submit.place(x=50, y=375)

clear = Button(lf, text='Clear fields', font=btn_font, bg=button_bg, width=20, command=databasefunctions.empty_fields)
clear.place(x=50, y=435)

# Right Top Frame
Button(rt, text='Delete book record', font=btn_font, bg=button_bg, width=17, command=databasefunctions.drop_info).place(x=8, y=30)
Button(rt, text='Delete full inventory', font=btn_font, bg=button_bg, width=17, command=databasefunctions.delete_info).place(x=178, y=30)
Button(rt, text='Update book details', font=btn_font, bg=button_bg, width=17,
       command=databasefunctions.upgrad_data).place(x=348, y=30)
Button(rt, text='Change Book Availability', font=btn_font, bg=button_bg, width=19,
       command=databasefunctions.alter_availability).place(x=518, y=30)

# Right Bottom Frame
Label(RB_frame, text='BOOK CATALOG', bg=rf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)

t = tk.Treeview(RB_frame, selectmode=BROWSE, columns=('Book Name', 'BookID', 'Author', 'Status', 'Issuer Card ID'))

XScrollbar = Scrollbar(t, orient=HORIZONTAL, command=t.xview)
YScrollbar = Scrollbar(t, orient=VERTICAL, command=t.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)

t.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

t.heading('Book Name', text='Book Name', anchor=CENTER)
t.heading('BookID', text='BookID', anchor=CENTER)
t.heading('Author', text='Author', anchor=CENTER)
t.heading('Status', text='Status of the Book', anchor=CENTER)
t.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)

t.column('#0', width=0, stretch=NO)
t.column('#1', width=225, stretch=NO)
t.column('#2', width=70, stretch=NO)
t.column('#3', width=150, stretch=NO)
t.column('#4', width=105, stretch=NO)
t.column('#5', width=132, stretch=NO)

t.place(y=60, x=0, relheight=1.0, relwidth=2)

databasefunctions.erase_and_show()

# Finalizing the window
root.update()
root.mainloop()
