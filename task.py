####################################
# Start virtual environment
# run - "taskenv/Scripts/activate"
# before starting project
####################################

# Project is a task tracker application.
# it will let me input tasks that i want to track
# and time stamp them, i should be able to
# log every event, 
# see a summary of past events logged,
# and delete tasks if need be. 

# a function is created to establish a 
# connection with the MySql database.
# Then i use that function to create a task database.
# the main table will have columns for
# primary key,
# task name,
# task category,
# date completed,
# completed by,
# task notes

# GUI will be a home screen that lets you 
# select from 1 of 3 options
# 1. Track Event
# 2. Delete/Edit Event
# 3. Event Summary
# with an emphasis on track event.

# Track Event will have an input field that takes the name of the text
# a drop down box to select which category you want to put the event under
# an input field for notes to attach to Event. 
# submit button. upon submittal the application will send a confirmation 
# message and ask if you want to add another event or return to the home screen

# Delete/Edit Event will pull up a list of events from the current month.
# each event will need a 'x' button to delete item and 'i' button to edit item. it will need a drop down box
# to look up events by month. and a submit button that will ask if user is 
# sure they want to change the selected events. Then return to the home screen.

# Event Summary will pull up a list of the current months events. 
# it will need a drop down box to pull up events by month.
# another drop down box to search events by category.
# A 'home' button to return to the home screen.

# initial gui will be tkinter but
# prefer to make flask or django app
# to incorporate html/css

import tkinter as tk
import logFunctions



        
# GUI section
root = tk.Tk()

root.geometry('700x500')
root.configure(bg='navyblue')

# header for home page
header = tk.Label(root, text="Event Tracker", font=('bold', 28), bg='navyblue', fg='white')
header.pack(pady='10px')
# subtext for header
p = "name and tag an event you want to track."
info = tk.Label(root, text=p, bg='navyblue', fg='white', font=14)
info.pack()
# main frame for nav buttons
mainframe = tk.Frame(root, bg='navyblue')
mainframe.pack()
# main button (Log Event) [grid position: (0, 0)]
logButton = tk.Button(mainframe, text="Log Event", bg='brown', 
                      fg='white', font=('bold', 30), command=logFunctions.eventLog)
logButton.grid(row=0, column=0, columnspan=2, 
         pady='10px', ipadx='25px', ipady='20px', sticky='ew')

# button to enter edit/delete screen
deleteButton = tk.Button(mainframe, text="Delete/Edit Event", bg='brown', fg='white', font=('bold', 18), command=logFunctions.eventEdit)
deleteButton.grid(row=1, column=0, pady='10px', ipadx='10px', ipady='10px')

# button to enter summary page
summaryButton = tk.Button(mainframe, text="Event Summary", bg='brown', fg='white', font=('bold', 18), command=logFunctions.eventSummary)
summaryButton.grid(row=1, column=1, padx='10px', pady='10px', ipadx='10px', ipady='10px')

root.mainloop()