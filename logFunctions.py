# creates table with columns for id, user, event, category, date completed, and notes.
# "CREATE TABLE IF NOT EXISTS events(id INT PRIMARY KEY AUTO_INCREMENT, user VARCHAR(25) NOT NULL, #event_name VARCHAR(50) NOT NULL, event_category VARCHAR(50) NOT NULL, date_completed DATE NOT NULL, notes VARCHAR(100));"

import tkinter as tk
from tkinter import messagebox, ttk
import sqlconnect
import calendar
import tkcalendar as tkc
from datetime import date, datetime
import sqlconnect
import helperFunctions


# main user hard coded until login screen is made
user = 'Cameron'
today = date.today()
monthNum = datetime.now().month
monthName = datetime.now().strftime("%B")
months = calendar.month_name[1:]


# function to log event
# input fields are nameEntry, categoryEntry, and notesEntry
# calls another funtion to query information
def eventLog():
    

    # first confirm that user wants to post displayed information
    # then log information to MySQL, clear the input fields and return to logger.
    def sqlLog(name, cat, date, note):
        name, cat, date, note = name.get(), cat.get(), date.get_date(), note.get(1.0, tk.END)
        m = f"Event Name: {name} \nEvent Category: {cat} \nDate: {date} \nNotes: {note} \n \nDo you wish to proceed?"
        prompt = messagebox.askyesno('Confirm Enrties', m)
        if prompt:
            with sqlconnect.mysqlconnect() as conn:
                with conn.cursor() as csr:
                    query = "INSERT INTO events(user, event_name, event_category, date_completed, notes) VALUES('%s', '%s', '%s', '%s', '%s');" %(user, name, cat, date, note.strip())
                    csr.execute(query)
                    print(query)
                    conn.commit()
                    nameEntry.delete(0, tk.END)
                    categoryEntry.set(" ")
                    notesEntry.delete(1.0, tk.END)
            
                    logLevel.destroy()
        else:
            return
        
    logLevel = tk.Toplevel()
    logLevel.configure(bg='navyblue')
    logLevel.geometry('500x450')
    logLevel.configure(bg='navyblue')
    
    #frame for packing
    logFrame = tk.Frame(logLevel, bg='navyblue')
    logFrame.pack(padx=20, pady=10)
    
    # header for event log
    logHeader = tk.Label(logFrame, text="Log Event", bg='navyblue', fg='goldenrod', font=('bold', 32))
    logHeader.grid(row=0, column=0, pady=(0, 15), columnspan=2)
    # event name
    nameLabel = tk.Label(logFrame, text="Event Name", bg='navyblue', fg='white')
    nameLabel.grid(row=1, column=0, columnspan=2)
    nameEntry = tk.Entry(logFrame, font=24)
    nameEntry.grid(row=2, column=0, columnspan=2, pady=(0, 10))
    # event category
    # categories = health, spiritual, career.
    categoryLabel = tk.Label(logFrame, text="Event Category", bg='navyblue', fg='white')
    categoryLabel.grid(row=3, column=0)
    categoryEntry = ttk.Combobox(logFrame, state='readonly', values=['Health', 'Spiritual', 'Career'], width=10)
    categoryEntry.grid(row=4, column=0)
    # date picker
    dateLabel = tk.Label(logFrame, text="Select Date *optional", bg='navyblue', fg='white')
    dateLabel.grid(row=3, column=1)
    dateEntry = tkc.DateEntry(logFrame, dateformat=2)
    dateEntry.grid(row=4, column=1)
    # notes for event
    notesLabel = tk.Label(logFrame, text="Add Notes", bg='navyblue', fg='white')
    notesLabel.grid(row=5, column=0, columnspan=2)
    notesEntry = tk.Text(logFrame, width=30, height=6, wrap='word', font=14, )
    notesEntry.grid(row=6, column=0, columnspan=2)
    
    info = [nameEntry, categoryEntry, dateEntry, notesEntry]
    # submit button
    submit = tk.Button(logFrame, text="Submit Event", bg='brown', fg='white', command=lambda: sqlLog(info[0], info[1], info[2], info[3]))
    submit.grid(row=7, column=0, sticky='ew', columnspan=2)
    
    #return button
    homeButton = tk.Button(logFrame, text="Home", bg='brown', fg='white', command=logLevel.destroy)
    homeButton.grid(row=8, column=0, pady=(25, 0), columnspan=2)
    



# function to edit or delete events
# eventEdit is the toplevel app
# miniEdit is the post destroyed screen for editing
# miniDelete just brings a pop up confirming deletion

def eventEdit():
    def miniDelete(sel):
        m = f"Delete from records?"
        ask = messagebox.askyesno("Confirm", m)
        if ask:
            sel = sel.get()
            with sqlconnect.mysqlconnect() as conn:
                with conn.cursor() as csr:
                    query = "DELETE FROM events WHERE id = %s" %sel 
                    csr.execute(query)
                    conn.commit()
            idx.delete(0, tk.END)
            editLevel.destroy()
            return messagebox.showinfo("Success", f"Event at id# {sel} deleted from records")
            
        else:
            return
        
    def miniEdit(sel):
        sel = sel.get()
        
        # function for editing selcted data
        def editConfirm(name, cat, date, note):
            vName, vCat, vDate, vNote = name.get(), cat.get(), date.get(), note.get(1.0, tk.END)
            print(name, cat, date, note)
            askingMessage = f"name: {vName} \ncategory: {vCat} \ndate: {vDate} \nnotes: {vNote} \n\nConfirm edits?"
            asking = messagebox.askyesno('Confirm', askingMessage)
            if asking:
                with sqlconnect.mysqlconnect() as conn:
                    with conn.cursor() as csr:
                        query1 = """
                        UPDATE events 
                        SET 
                            event_name = '%s',
                            event_category = '%s',
                            date_completed = '%s',
                            notes = '%s'
                        WHERE
                            id = %s""" %(vName.strip(), vCat, vDate, vNote, sel)
                        csr.execute(query1)
                        conn.commit()
                messagebox.showinfo("Success", "Succesfully updated event record")
                editLevel.destroy()
            else:
                editLevel.destroy()
                eventEdit()
                
            # end editRow

        with sqlconnect.mysqlconnect() as conn:
            with conn.cursor() as csr:
                query = f"SELECT event_name, event_category, date_completed, notes FROM events WHERE id = {sel}"
                csr.execute(query)
                # selected data includes name, category, date, and notes from 
                # single line
                selectedData = csr.fetchone()
                print(selectedData)
            
        
        displayBoard.destroy()
        deleteButton.destroy()
        idx.destroy()
        idxLabel.destroy()
        monthPicker.destroy()
        editButton.destroy()
        eventNameLabel = tk.Label(editFrame, text="Event Name", bg='navyblue', fg='white')
        eventNameLabel.grid(row=2, column=0)
        eventName = tk.Entry(editFrame)
        eventName.insert(0, selectedData[0])
        eventName.grid(row=2, column=1)
        eventCatLabel = tk.Label(editFrame, text="Category", bg='navyblue', fg='white')
        eventCatLabel.grid(row=3, column=0)
        eventCat = ttk.Combobox(editFrame, state='readonly', values=['Health', 'Spiritual', 'Career'], width=10)
        eventCat.set(selectedData[1])
        eventCat.grid(row=3, column=1)
        eventDateLabel = tk.Label(editFrame, text="Log Date", bg='navyblue', fg='white')
        eventDateLabel.grid(row=4, column=0)
        eventDate = tk.Entry(editFrame)
        eventDate.insert(0, str(selectedData[2]))
        eventDate.grid(row=4, column=1)
        eventNotesLabel = tk.Label(editFrame, text="Notes", bg='navyblue', fg='white')
        eventNotesLabel.grid(row=5, column=0)
        eventNotes = tk.Text(editFrame, width=20, height=4, wrap='word')
        eventNotes.insert(1.0, selectedData[3])
        eventNotes.grid(row=5, column=1)
        # new button
        finalEditButton = tk.Button(editFrame, text='Confirm Changes', bg='brown', fg='white', command=lambda x=eventName, y=eventCat, z=eventDate, a=eventNotes: editConfirm(x, y, z, a))
        finalEditButton.grid(row=6, column=1, columnspan=2)
        ################
        #########
        ### end miniEdit
        
    # get data from db and store values in 'selected' variable
    with sqlconnect.mysqlconnect() as conn:
        with conn.cursor() as csr:
            query = "SELECT id, event_name, date_completed FROM events WHERE MONTH(date_completed)=%s"%monthNum
            csr.execute(query)
            selected = csr.fetchall()
        
    
    editLevel = tk.Toplevel()
    editLevel.configure(bg='navyblue')
    editLevel.geometry('500x450')
    editLevel.configure(bg='navyblue')
    # editor main frame
    editFrame = tk.Frame(editLevel, bg='navyblue')
    editFrame.pack()
    # editor header
    editHeader = tk.Label(editFrame, bg='navyblue', fg='goldenrod', text="Event Editor", font=('bold', 24))
    editHeader.grid(row=0, column=0, pady=(10, 0), columnspan=2)
    # choose month to display (default current month)
    monthPicker = ttk.Combobox(editFrame, values=[i for i in months])
    monthPicker.set(monthName)
    monthPicker.grid(row=1, column=0, columnspan=2)
    # display board for Events from 'selected' variable
    displayBoard = tk.Text(editFrame, height=12, width=45, wrap='word')
    displayBoard.grid(row=2, column=0, columnspan=2)
    for s in selected:
        displayBoard.insert(tk.END, f"id: {s[0]} | EVENT: {s[1]} | DATE: {s[2]} \n\n")
    # entry for selected row
    idxLabel = tk.Label(editFrame, text="select id to edit/delete", bg='navyblue', fg='white')
    idxLabel.grid(row=3, column=0)
    idx = tk.Entry(editFrame, width=5)
    idx.grid(row=3, column=1)
    
        
    # Buttons
    editButton = tk.Button(editFrame, text="Edit", bg='brown', fg='white', command=lambda x=idx: miniEdit(x))
    editButton.grid(row=4, column=0, pady=(15, 0))
    deleteButton = tk.Button(editFrame, text="Delete", bg='brown', fg='white', command=lambda x=idx: miniDelete(x))
    deleteButton.grid(row=4, column=1, pady=(15, 0))
    


# current task
# inner function to pull month name and return 
# sql data. 
# currently stuck on converting month name to int for sql query
# solved by creating helperfunction.name2num()
        
def eventSummary():
    dataset = []
    
    def insertData(x):
        dataset.clear()
        n = helperFunctions.name2num(byMonth.get())
        with sqlconnect.mysqlconnect() as conn:
            with conn.cursor() as csr:
                q = "SELECT event_name, date_completed, notes FROM events WHERE MONTH(date_completed) = %s"%n
                csr.execute(q)
                byMonthGet = csr.fetchall()
        for i in byMonthGet:
            for _ in i:
                dataset.append(str(_))
                        
        
        
    def initial():   
        with sqlconnect.mysqlconnect() as conn:
            with conn.cursor() as csr:
                sumQuery = "SELECT event_name, date_completed, notes FROM events WHERE MONTH(date_completed)=%s;"%monthNum
                csr.execute(sumQuery)
                data = csr.fetchall()
                        
        for i in data:
            for _ in i:
                dataset.append(str(_))
    
    initial()
    summaryLevel = tk.Toplevel()
    summaryLevel.configure(bg='navyblue')
    summaryLevel.geometry('500x450')
    summaryLevel.configure(bg='navyblue')
    
    summaryFrame = tk.Frame(summaryLevel, bg='navyblue')
    summaryFrame.pack()
    
    summaryHeader = tk.Label(summaryFrame, bg='navyblue', fg='white', text="Event Summary")
    summaryHeader.grid(row=0, column=0, columnspan=2)
    
    byMonthLabel = tk.Label(summaryFrame, bg='navyblue', fg='white', text="By Month")
    byMonthLabel.grid(row=1, column=0, columnspan=2)
    ###############################
    varText = tk.StringVar()
    byMonth = ttk.Combobox(summaryFrame, state='readonly', textvariable=varText)
    byMonth['values'] = [i for i in months]
    byMonth.current(monthNum-1)
    byMonth.grid(row=2, column=0)
    byMonth.bind("<<ComboboxSelected>>", insertData)
    ###############################
    # sumButton = tk.Button(summaryFrame, text="Search", bg='brown', fg='white', command=lambda x=varText.get(): insertData(x))
    # sumButton.grid(row=2, column=1, padx=(5, 0))
    
    
    displayFrame = tk.Frame(summaryFrame, bg='navyblue')
    displayFrame.grid(row=3, column=0)
    
    labels = len(dataset)
    for label in range(labels):
        tk.Label(displayFrame, bg='navyblue', fg='white', text=[i for i in dataset]).pack()
        
    
    
    
    
    
         
    
        