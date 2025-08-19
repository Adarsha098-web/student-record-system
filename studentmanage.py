import sqlite3
from tkinter import *
from tkinter import ttk, messagebox as mb
from tkcalendar import DateEntry

# DB Setup
connector = sqlite3.connect("student_management.db")
cursor = connector.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT_MANAGEMENT (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME TEXT NOT NULL,
    EMAIL TEXT,
    PHONE_NO TEXT,
    GENDER TEXT,
    DOB TEXT,
    STREAM TEXT
)
""")
connector.commit()


# Functions
def clear_fields():
    for var in [name_strvar, email_strvar, contact_strvar, gender_strvar, stream_strvar]:
        var.set('')
    dob.set_date('2000-01-01')


def display_records():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM STUDENT_MANAGEMENT")
    for row in cursor.fetchall():
        tree.insert('', END, values=row)


def add_record():
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    dob_str = dob.get_date().strftime("%Y-%m-%d")
    stream = stream_strvar.get()

    if not name or not email or not contact or not gender or not dob_str or not stream:
        mb.showerror("Input Error", "All fields are required.")
        return

    try:
        cursor.execute("""
            INSERT INTO STUDENT_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, contact, gender, dob_str, stream))
        connector.commit()
        display_records()
        mb.showinfo("Success", "Record added successfully!")
        clear_fields()
    except Exception as e:
        mb.showerror("Database Error", str(e))


def delete_record():
    selected = tree.selection()
    if not selected:
        mb.showerror("Error", "Select a record to delete.")
        return
    record = tree.item(selected)['values'][0]
    cursor.execute("DELETE FROM STUDENT_MANAGEMENT WHERE ID = ?", (record,))
    connector.commit()
    display_records()
    mb.showinfo("Success", "Record deleted successfully!")


def view_record():
    selected = tree.selection()
    if not selected:
        mb.showerror("Error", "Select a record to view.")
        return
    row = tree.item(selected)['values']
    name_strvar.set(row[1])
    email_strvar.set(row[2])
    contact_strvar.set(row[3])
    gender_strvar.set(row[4])
    dob.set_date(row[5])
    stream_strvar.set(row[6])


def update_record():
    selected = tree.selection()
    if not selected:
        mb.showerror("Error", "Select a record to update.")
        return
    record_id = tree.item(selected)['values'][0]
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    dob_str = dob.get_date().strftime("%Y-%m-%d")
    stream = stream_strvar.get()

    cursor.execute("""
        UPDATE STUDENT_MANAGEMENT SET NAME=?, EMAIL=?, PHONE_NO=?, GENDER=?, DOB=?, STREAM=?
        WHERE ID=?
    """, (name, email, contact, gender, dob_str, stream, record_id))
    connector.commit()
    display_records()
    mb.showinfo("Success", "Record updated successfully!")
    clear_fields()


# GUI
main = Tk()
main.title("Student Management System")
main.state('zoomed')  # Open in maximized mode

# Variables
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()

# Layout
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=2)
main.rowconfigure(0, weight=1)

left_frame = Frame(main, padx=20, pady=20)
left_frame.grid(row=0, column=0, sticky='nswe')
right_frame = Frame(main, padx=20, pady=20)
right_frame.grid(row=0, column=1, sticky='nswe')

for i in range(20):
    left_frame.rowconfigure(i, weight=1)

Label(left_frame, text="Name:", font=('Arial', 12)).grid(row=0, column=0, sticky=W)
Entry(left_frame, textvariable=name_strvar, font=('Arial', 12), width=30).grid(row=0, column=1)

Label(left_frame, text="Email:", font=('Arial', 12)).grid(row=1, column=0, sticky=W)
Entry(left_frame, textvariable=email_strvar, font=('Arial', 12), width=30).grid(row=1, column=1)

Label(left_frame, text="Contact No:", font=('Arial', 12)).grid(row=2, column=0, sticky=W)
Entry(left_frame, textvariable=contact_strvar, font=('Arial', 12), width=30).grid(row=2, column=1)

Label(left_frame, text="Gender:", font=('Arial', 12)).grid(row=3, column=0, sticky=W)
ttk.Combobox(left_frame, textvariable=gender_strvar, values=['Male', 'Female', 'Other'], font=('Arial', 12), width=28).grid(row=3, column=1)

Label(left_frame, text="Date of Birth:", font=('Arial', 12)).grid(row=4, column=0, sticky=W)
dob = DateEntry(left_frame, date_pattern='yyyy-mm-dd', font=('Arial', 12), width=28)
dob.grid(row=4, column=1)

Label(left_frame, text="Stream:", font=('Arial', 12)).grid(row=5, column=0, sticky=W)
Entry(left_frame, textvariable=stream_strvar, font=('Arial', 12), width=30).grid(row=5, column=1)

Button(left_frame, text="Submit and Add Record", font=('Arial', 12), command=add_record, bg='green', fg='white').grid(row=6, column=0, columnspan=2, pady=10, sticky='ew')
Button(left_frame, text="Clear Fields", font=('Arial', 12), command=clear_fields).grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
Button(left_frame, text="Delete Record", font=('Arial', 12), command=delete_record, bg='red', fg='white').grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')
Button(left_frame, text="View Record", font=('Arial', 12), command=view_record).grid(row=9, column=0, columnspan=2, pady=10, sticky='ew')
Button(left_frame, text="Update Record", font=('Arial', 12), command=update_record, bg='orange').grid(row=10, column=0, columnspan=2, pady=10, sticky='ew')

# Right Frame Treeview
tree = ttk.Treeview(right_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Gender', 'DOB', 'Stream'), show='headings')
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=120)
tree.pack(expand=True, fill='both')

# Initial Display
display_records()
main.mainloop()
