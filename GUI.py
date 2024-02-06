from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import messagebox
import mysql.connector


def get_user():
    user_list = []
    for user in user_table:
        user_list.append(user[1])
    global user_id
    user_id = entry.get()
    if len(user_id) != 0 and user_id in user_list:
        my_cursor.execute("SELECT DISTINCT c.cname, last_read FROM comics as c JOIN emails as e ON c.cname = e.cname "
                          "WHERE e.email_id = '" + user_id + "' ORDER BY c.last_read")
        global comic_table
        comic_table = my_cursor.fetchall()

        entry.pack_forget()
        submit_button.pack_forget()
        entry_label.pack_forget()

        print('welcome')
        # <editor-fold desc="Add Widgets to Window">
        notebook.add(add_tab, text="Add")
        notebook.add(remove_tab, text="Remove")
        notebook.add(last_read_tab, text="Last Read")
        notebook.pack(expand=True, side='bottom', fill="both")

        add_canvas.pack()
        remove_canvas.pack()
        last_canvas.pack()
        add_canvas.create_image(0, 0, image=back_img1, anchor=NW)
        remove_canvas.create_image(0, 0, image=back_img2, anchor=NW)
        last_canvas.create_image(0, 0, image=back_img3, anchor=NW)

        add_canvas.create_window(20, 50, window=search_entry1, anchor=W)
        found_titles.place(x=0, y=100)
        search_button1.place(x=400, y=30)
        add_button.place(x=200, y=400)

        remove_canvas.create_window(20, 50, window=search_entry2, anchor=W)
        remove_button.place(x=175, y=400)
        search_button2.place(x=400, y=30)
        existing_titles.place(x=0, y=100)

        last_read_title.place(x=0, y=50)
        last_read_date.place(x=256, y=50)
        message_log3.place(x=20, y=18)
        message_log4.place(x=270, y=18)

        i = 0
        for comic in comic_table[0:10]:
            existing_titles.insert(i, comic[0])
            last_read_title.insert(i, comic[0])
            if comic[1] is None:
                last_read_date.insert(i, "None")
            else:
                last_read_date.insert(i, comic[1])
            i += 1
        # </editor-fold>
    else:
        messagebox.showerror(title="ERROR", message="USER NOT FOUND!")
        print('user not found')


def add_title():
    try:
        if found_titles.curselection():
            comic_title = found_titles.get(found_titles.curselection())
            sql = "INSERT INTO emails (cname, email_id) VALUES (%s, %s)"
            val = (comic_title, user_id)
            my_cursor.execute(sql, val)
            mydb.commit()
            message_log1.config(text="ADDED SUCCESSFULLY")
            print("title added")
        else:
            message_log1.config(text="No title has been selected!")
    except mysql.connector.errors.IntegrityError:
        message_log1.config(text="TITLE ALREADY EXISTS")
        print("TITLE ALREADY EXISTS!")
    message_log1.place(x=20, y=300)


def search_title():
    print("searching...")
    message_log1.place_forget()
    found_titles.delete(0, found_titles.size())

    search_item = search_entry1.get()
    my_cursor.execute("SELECT cname FROM comics where cname LIKE '%" + search_item + "%'")
    result = my_cursor.fetchall()

    if len(result) == 0:
        message_log1.config(text="NO TITLE FOUND!")
        message_log1.place(x=20, y=150)
    else:
        i = 0
        for item in result[0:10]:
            found_titles.insert(i, item[0])
            i += 1
    found_titles.config(height=found_titles.size())


def remove_title():
    if existing_titles.curselection():
        comic_title = existing_titles.get(existing_titles.curselection())
        my_cursor.execute("DELETE FROM emails WHERE cname = '" + comic_title + "'")
        mydb.commit()
        message_log2.config(text="REMOVED SUCCESSFULLY")
        print("title removed")
        find_title()
    else:
        message_log2.config(text="NO TITLE SELECTED!")
    message_log2.place(x=20, y=300)


def find_title():
    message_log2.place_forget()
    existing_titles.delete(0, existing_titles.size())

    search_item = search_entry2.get()
    my_cursor.execute("SELECT cname FROM emails where cname LIKE '%" + search_item +
                      "%' and email_id = '" + user_id + "'")
    result = my_cursor.fetchall()

    if len(result) == 0:
        message_log2.config(text="NO TITLES FOUND!")
        message_log2.place(x=20, y=150)
    else:
        i = 0
        for item in result[0:10]:
            existing_titles.insert(i, item[0])
            i += 1
    existing_titles.config(height=existing_titles.size())
    print("found")


window = Tk()
icon = PhotoImage(file='app_icon.png')
window.title("Notification Manager")
window.iconphoto(True, icon)
window.config(bg='black')
user_id = ''

# Establish connection with mySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1@nc310t",
    database="notification"
)
my_cursor = mydb.cursor()

# <editor-fold desc="Window Style">
style_config = Style()
style_config.theme_use('default')

style_config.configure('TNotebook',
                       background='dark',
                       borderwidth=0)
style_config.configure('TNotebook.Tab',
                       font=('Courier', '20', 'bold'),
                       background='#1c1c1b',
                       foreground='white',
                       padding=[10, 2],
                       borderwidth=.5)
style_config.map('TNotebook.Tab', background=[('selected', '#4bbf45')])
# </editor-fold>
# <editor-fold desc="Login UI">
entry_label = Label(window,
                    text="Enter EmailID:",
                    font=('Courier', '17', 'bold'),
                    bg='black',
                    fg='#4bbf45')
entry = Entry(window,
              font=('Courier', '20'),
              bg='black',
              fg='white')
submit_button = Button(window,
                       text="Submit",
                       font=('Courier', '12', 'bold'),
                       fg='white',
                       bg='#4bbf45',
                       activeforeground='white',
                       activebackground='black',
                       command=get_user)
entry_label.pack(side='left')
entry.pack(side='left')
submit_button.pack(side='right')
# </editor-fold>
# <editor-fold desc="GUI Widgets">
notebook = ttk.Notebook(window)
add_tab = Frame(notebook)
remove_tab = Frame(notebook)
last_read_tab = Frame(notebook)

add_canvas = Canvas(add_tab, width=512, height=512)
back_img1 = PhotoImage(file='yellow.png')
remove_canvas = Canvas(remove_tab, width=512, height=512)
back_img2 = PhotoImage(file='red.png')
last_canvas = Canvas(last_read_tab, width=512, height=512)
back_img3 = PhotoImage(file='blue.png')

search_entry1 = Entry(add_canvas, font=('Courier', '20'), background='#f2d055')
search_entry2 = Entry(remove_canvas, font=('Courier', '20'), background='#f58e53')
search_button1 = Button(add_canvas,
                        text="Search",
                        font=('Courier', '15', 'bold'),
                        fg='black',
                        bg='#f2d055',
                        activeforeground='black',
                        activebackground='#f29f3f',
                        command=search_title)
search_button2 = Button(remove_canvas,
                        text="Search",
                        font=('Courier', '15', 'bold'),
                        fg='black',
                        bg='#f58e53',
                        activeforeground='black',
                        activebackground='#fa5a41',
                        command=find_title)
add_button = Button(add_canvas,
                    text="Add Title",
                    font=('Courier', '15', 'bold'),
                    fg='black',
                    bg='#f2d055',
                    activeforeground='black',
                    activebackground='#f29f3f',
                    command=add_title)
remove_button = Button(remove_canvas, text="Remove Title",
                       font=('Courier', '15', 'bold'),
                       fg='black',
                       bg='#f58e53',
                       activeforeground='black',
                       activebackground='#fa5a41',
                       command=remove_title)
found_titles = Listbox(add_canvas,
                       font=('Courier', '15', 'bold'),
                       background='#f2d055',
                       selectbackground='#f29f3f',
                       width=100)
existing_titles = Listbox(remove_canvas,
                          font=('Courier', '15', 'bold'),
                          background='#f58e53',
                          selectbackground='#fa5a41',
                          width=100)
last_read_title = Listbox(last_canvas,
                          font=('Courier', '15', 'bold'),
                          background='#317094',
                          selectbackground='#153547',
                          width=100)
last_read_date = Listbox(last_canvas,
                         font=('Courier', '15', 'bold'),
                         background='#317094',
                         selectbackground='#153547',
                         width=100)
message_log1 = Label(add_canvas,
                     text="NO TITLES FOUND!",
                     font=('Courier', '15', 'bold'),
                     bg='#f2d055',
                     fg='black')
message_log2 = Label(remove_canvas,
                     text="NO TITLES FOUND!",
                     font=('Courier', '15', 'bold'),
                     bg='#f58e53',
                     fg='black')
message_log3 = Label(last_canvas,
                     text="COMIC NAME",
                     font=('Courier', '15', 'bold'),
                     bg='#317094',
                     fg='black')
message_log4 = Label(last_canvas,
                     text="DATE",
                     font=('Courier', '15', 'bold'),
                     bg='#317094',
                     fg='black')
# </editor-fold>

my_cursor.execute("SELECT * FROM users")
user_table = my_cursor.fetchall()
my_cursor.execute("SELECT * FROM comics")
comic_table = my_cursor.fetchall()

window.resizable(False, False)
window.mainloop()
