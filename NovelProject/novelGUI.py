"""
Tung Hoang - 03/12/20
The following program is the GUI of a book searching and adding application.
The user will be able to request a book report and add a new book from existing writer

Citation:
Tabulate table: https://pypi.org/project/tabulate/#files
"""

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
from tabulate import tabulate

#model
import sqlite3 as sq

con = sq.connect("../NovelProject/novel.db")
c = con.cursor()

def get_count_book():
    res = c.execute("SELECT COUNT(*) from Book")
    data = c.fetchall() # Gets the data from the table
    return data

def get_writers():
    res = c.execute("SELECT * from Writer")
    data = c.fetchall() # Gets the data from the table
    return data

def check_writer(wtid):
    res = c.execute("SELECT WriterID from Writer")
    writerIDs = c.fetchall() # Gets the data from the table
    for wt in writerIDs:
        if wtid in wt:
            return True
    return False

def check_book(t, g, w):
    dataSet = (str(t), str(g), int(w))
    res = c.execute("SELECT Title, Genre, WriterID from Book")
    bookData = c.fetchall() # Gets the data from the table
    
    if dataSet in bookData:
        return True
    else:
        return False
    
def get_books():
    res = c.execute("SELECT BookID, Title, Genre, Name FROM Book, Writer WHERE Book.WriterID = Writer.WriterID;")
    data = c.fetchall() # Gets the data from the table
    return data

def add_book(book, title, genre, writer):
    c.execute("INSERT INTO Book (BookID, Title, Genre, WriterID) Values (?, ?, ?, ?);",(str(book), str(title), str(genre), str(writer)))
    con.commit()        #DO THIS COMMIT ANY TIME YOU CHANGE THE DATABASE - after a complete transaction!!!



def render_menu():
    window = Tk()
    window.title("Sailor Main Menu")
    window.geometry("200x100")
    rpt = Button(window, text="Get Report", command = render_book_report)
    rpt.pack()

    res = Button(window, text="Adding a book", command = render_adding_request)
    res.pack()

    ext = Button(window, text="Exit", command = lambda:end_program(window))
    ext.pack()
    window.mainloop()
     
def end_program(w):
    con.close()
    messagebox.showinfo('Thank you', 'Thank you for using the application')
    w.destroy()
    

def render_book_report():
    # This report is pretty!
    res_rep_win = Tk()
    res_rep_win.title("Book Report")
    res_rep_win.geometry("600x250")

    book_frame = Frame(res_rep_win)
    book_frame.pack()
    
    books = get_books()
    tbl = tabulate(books, headers=['BookID','Title','Genre','Author'], tablefmt='orgtbl')
    lbl = Label(book_frame, text = tbl, justify = LEFT, font = ('courier', 12)).pack()
    
    res_rep_win.mainloop()


def render_adding_request():

    res_add_win = Tk()
    res_add_win.title("Novel Adding Request")
    res_add_win.geometry("400x400")

    info_frame = Frame(res_add_win)
    info_frame.pack(side = LEFT)

    bookID = int(get_count_book()[0][0]) + 1
    ttl = tk.StringVar(res_add_win)
    gnr = tk.StringVar(res_add_win)

    
    lbl = Label(info_frame, text = "Choose a writer, title, and genre").pack()
    
    lblttl = Label(info_frame, text = "Title").pack()
    title = Entry(info_frame, text="Book title", textvariable = ttl).pack()

    lblgnr = Label(info_frame, text = "Genre").pack()
    genre = Entry(info_frame, text="Book Genre", textvariable = gnr).pack()


    option_frame = Frame(res_add_win)
    option_frame.pack(side = RIGHT)

    # This will populate the writer listbox
    writers = get_writers()
    writerlb = writer_lb(res_add_win, option_frame, writers)

    rpt = Button(info_frame, text="Add Book",
                 command = lambda: check_and_enter_book(bookID, ttl.get(), gnr.get(),
                            writers[writerlb.curselection()[0]][0])).pack()

    

   
    
    res_add_win.mainloop()

def check_and_enter_book(bk, t, g, w):
    
    if not(check_book(t, g, w)):
        add_book(bk, t, g, w)
        messagebox.showinfo("Success!", "Your book has been added!")
    else:
        messagebox.showerror("Error!", "Possible errors:  \nThe book is already register \n")
        return



def writer_lb(w,f, writers):
    lblwriter = Label(f,text = "WriterID, Writer").pack(side = TOP)

    Lb = Listbox(f, height = 8, width = 26,font=("arial", 12), exportselection = False) 
    Lb.pack(side = TOP, fill = Y)
                
    scroll = Scrollbar(w, orient = VERTICAL) # Set scrollbar to list box for when entries exceed size of list box
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)
    

    i = 0
    for writer in writers:
        Lb.insert(i, writer)
        i += 1
    Lb.selection_set(first = 0)

    return Lb


render_menu()

