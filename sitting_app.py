"""
Sitting is the new smoking.
"""
import sys
import time
import pandas as pd

# import sqlite3
# from sqlite3 import Error

from tkinter import *
# from tkinter import messagebox

import csv
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
#from datetime import datetime

"""class SittingApp(tk.Tk):
    def __init__(self):
        container = Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weigth=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        for largeF in (CounterPage,PlotPage):
            framy = largeF(container,self)
            self.frames[largeF] = framy
            framy.grid(row=0,column=0,sticky="nsew")
        self.show_page(CounterPage)

    def show_page(self,thisClass):
        frame = self.frames[thisClass]
        frame.tkraise() 

    def get_page(self,page_class):
        return self.frames[page_class]
"""

#create TK window

root=Tk()
root.geometry("200x200")
root.title("Avoid sitting")
root.resizable(0,0)

hr = StringVar()
mi = StringVar()
sec = StringVar()
warn = StringVar()
filename = r"sitting_time.csv"

xPos=30
yPos=20
offset=35
myFont = ("Arial",12,"")

"""Yes! sqlite is installed

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(':memory:')
        print("SQLite ver.",sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
 
create_connection()
"""

if len(sys.argv) <= 1:
    print("A valid date is required (YYYY/MM/DD)")
    exit()

_date = sys.argv[1]

# aux_date = _date.split("/")

msg = Label(root,text="Reduce your sitting time",foreground='#0000ff',font=myFont)
msg.place(x=xPos-10,y=160)

warn_msg = Label(root,text="",foreground="#ff0000",font=myFont,textvariable=warn)
warn_msg.place(x=xPos,y=yPos+2*offset)

hrEntry = Entry(root,width=3,font=("Arial",18,""),textvariable=hr,justify="right")
hrEntry.place(x=xPos,y=yPos)
hrLabel = Label(root,text="HRS")
hrLabel.place(x=xPos+10,y=yPos+offset)

miEntry = Entry(root,width=3,font=("Arial",18,""),textvariable=mi,justify="right")
miEntry.place(x=xPos+50,y=yPos)
miLabel = Label(root,text="MINS")
miLabel.place(x=xPos+60,y=yPos+offset)

secEntry = Entry(root,width=3,font=("Arial",18,""),textvariable=sec,justify="right")
secEntry.place(x=xPos+100,y=yPos)
secLabel = Label(root,text="SECS")
secLabel.place(x=xPos+110,y=yPos+offset)

got_time = 0
hr.set("00")
mi.set("00")
sec.set("00")
 
def init_values():
    hrEntry.delete(0,END)
    hrEntry.insert(0, "00")
    miEntry.delete(0,END)
    miEntry.insert(0,"00")
    secEntry.delete(0,END)
    secEntry.insert(0,"00")
    got_time = 0


def submit(temp=0):
    try:
        temp = int(hr.get())*3600 + int(mi.get())*60+int(sec.get())
    except:
        print("Please input the right value")

    while temp > -1:
        # > -1, temp -=1
        mins,secs = divmod(temp,60)
        hours = 0
        if mins > 60:
            hours,mins = divmod(mins,60)

        if temp > 60*35:
            miEntry.config({"background":"#ffff00"})
            secEntry.config({"background":"#ffff00"})
            warn.set("Get up and stand up!")
        else:
            miEntry.config({"background":"#ffffff"})
            secEntry.config({"background":"#ffffff"})
            warn.set("")

        # hr.set("{0:2d}".format(hours))
        hr.set("{:02d}".format(hours))
        mi.set("{:02d}".format(mins))
        sec.set("{:02d}".format(secs))
        root.update()
        time.sleep(1)

        # if (temp==0):
        #     messagebox.showinfo("Time countdown","Sorry, time's up")
        temp += 1
 

def stop_timer():
    # when leaving sit, should store time into string an display on Label
    sit_time = hrEntry.get() + ":" + miEntry.get() + ":" + secEntry.get()
    curr_time = time.localtime() #datetime.now()
    # must read file and then append new time
    # with open("sat_time.txt") as satFile:
    #
    date_n_time = _date.replace("/", "-") + " " + time.strftime("%H:%M",curr_time)
    stopped = [date_n_time,sit_time]
    write_info(stopped)
    # print(stopped)

    init_values()
    submit(got_time)
 

def write_info(new_data):
    """with open(filename,"r") as inFile:
        data = csv.reader(inFile,delimiter=',')
        for row in data:
            print(row)"""

    with open (filename,'a',newline='') as outFile:
        add_data = csv.writer(outFile,delimiter=',')
        add_data.writerow(new_data)


def plot_data(parent):
    figure = Figure(figsize=(6,4),dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure,master=parent)
    # NavigationToolbar2Tk(figure_canvas)
    axes = figure.add_subplot()

    df = pd.read_csv(filename,parse_dates=['date'])
    # Parsing time from string type to dateTime type:
    # pd.to_datetime(df['sitting_time'],format="%H:%M:%S")
    # actually the above added date=1900,01,01 to each time
    # the following works cuz splits string and calcs time in minutes
    df['sit_mins']=df['sitting_time'].str.split(':').apply(lambda x:int(x[0])*60+int(x[1])+int(x[2])/60)

    axes.bar(df['date'],df['sit_mins'])
    figure_canvas.draw()

    figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH,expand=1)

 
def create_window():
    newWindow = Toplevel()
    return newWindow

 
if __name__ == "__main__":
    print("Please do NOT close this window")
    init_values()
    btn = Button(root,text="Plot",bd='1',font=myFont,command=lambda:plot_data(create_window()))

    btn.pack(side="right")
    #lambda:submit(0)
    btn.place(x=xPos-10,y=120)

    stop_btn = Button(root,text="Stop",bd='1',font=myFont,command=stop_timer)
    stop_btn.place(x=130,y=120)

    submit(0)

    root.mainloop()
