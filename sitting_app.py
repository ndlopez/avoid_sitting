"""
Sitting is the new smoking
"""
import sys
import time
import pandas as pd
# import sqlite3
# from sqlite3 import Error
import tkinter as tk
from tkinter import filedialog, ttk
# from tkinter import messagebox
import csv
import matplotlib
import matplotlib.dates as mdates
import subprocess

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
   FigureCanvasTkAgg, NavigationToolbar2Tk
)
#from datetime import datetime
filename = "sitting_time.csv"

if len(sys.argv) <= 1:
       print("A valid date is required (YYYY/MM/DD)")
       exit()

_date = sys.argv[1]

class SittingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200")
        self.title("Avoid sitting")
        self.resizable(0,0)
        self.DEFAULT_COLOR = self.cget('bg')
        self.hr = tk.StringVar()
        self.mi = tk.StringVar()
        self.sec = tk.StringVar()
        self.warn = tk.StringVar()

        self.build_widgets()
        self.init_values()
        self.submit(0)

        self.protocol("WM_DELETE_WINDOW",self.destroy)
        """container = Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weigth=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        for largeF in (CounterPage,PlotPage):
            framy = largeF(container,self)
            self.frames[largeF] = framy
            framy.grid(row=0,column=0,sticky="nsew")
        self.show_page(CounterPage)"""
   
    def show_page(self,thisClass):
        frame = self.frames[thisClass]
        frame.tkraise()

    def get_page(self,page_class):
        return self.frames[page_class]

    def build_widgets(self):
        offset=35
        xPos = 30
        yPos = 20
        myFont = ("Arial",12,"")
        self.bot_msg = ttk.Label(self,text="Reduce your sitting time",foreground='#0000ff',font=myFont)
        self.bot_msg.place(x=xPos-10,y=160)

        self.warn_msg = ttk.Label(self,text="",foreground="#ff0000", font=myFont,textvariable=self.warn)
        self.warn_msg.place(x=xPos,y=yPos+2*offset)

        self.hrEntry = tk.Entry(self,width=3,font=("Arial",18,""),textvariable=self.hr,justify="right")
        self.hrEntry.place(x=xPos,y=yPos)
        hrLabel = ttk.Label(self,text="HRS")
        hrLabel.place(x=xPos+10,y=yPos+offset)

        self.miEntry = tk.Entry(self,width=3,font=("Arial",18,""),textvariable=self.mi,justify="right")
        self.miEntry.place(x=xPos+50,y=yPos)
        miLabel = ttk.Label(self,text="MINS")
        miLabel.place(x=xPos+60,y=yPos+offset)

        self.secEntry = tk.Entry(self,width=3,font=("Arial",18,""),textvariable=self.sec,justify="right")
        self.secEntry.place(x=xPos+100,y=yPos)
        secLabel = ttk.Label(self,text="SECS")
        secLabel.place(x=xPos+110,y=yPos+offset)

        stop_btn = tk.Button(self,text="Stop",bd='1',font=myFont,command=self.stop_timer)
        stop_btn.place(x=130,y=120)
        btn = tk.Button(self,text="Plot",bd='1',font=myFont,command=lambda:plot_data(create_window()))
        btn.pack(side="right")
        #lambda:submit(0)
        btn.place(x=xPos-10,y=120)

        self.got_time = 0
        self.hr.set("00")
        self.mi.set("00")
        self.sec.set("00")

    def init_values(self):
        self.hrEntry.delete(0,tk.END)
        self.hrEntry.insert(0, "00")
        self.miEntry.delete(0,tk.END)
        self.miEntry.insert(0,"00")
        self.secEntry.delete(0,tk.END)
        self.secEntry.insert(0,"00")
        self.got_time = 0
   
    def submit(self,temp=0):
        upTime = 40 #minutes
        try:
            temp = int(self.hr.get())*3600 + int(self.mi.get())*60 + int(self.sec.get()) #seconds
        except:
            print("Please do NOT input any values")
        while temp > -1:
            # > -1, temp -=1
            mins,secs = divmod(temp,60)
            hours = 0
            if mins > 59:
                hours,mins = divmod(mins,60)

            if temp > 60*upTime:
                # miEntry.config({"background":"#ffff00"})
                # secEntry.config({"background":"#ffff00"})
                self.configure(bg='yellow')
                self.bot_msg.config({"background":"#ffff00"})
                self.warn_msg.config({"background":"#ffff00"})
                self.warn.set("Get up and stand up!")
                # this function runs every second until STOP btn is pressed
                # run_popUp(str(upTime))
                self.attributes("-topmost", True)
            else:
                # miEntry.config({"background":"#ffffff"})
                # secEntry.config({"background":"#ffffff"})
                self.configure(bg=self.DEFAULT_COLOR)
                self.bot_msg.config({"background":self.DEFAULT_COLOR})
                self.warn_msg.config({"background":self.DEFAULT_COLOR})
                self.warn.set("")
                self.attributes("-topmost", False)

            # hr.set("{0:2d}".format(hours))
            self.hr.set("{:02d}".format(hours))
            self.mi.set("{:02d}".format(mins))
            self.sec.set("{:02d}".format(secs))
            self.update()
            time.sleep(1)

            # if (temp==0):
            #     messagebox.showinfo("Time countdown","Sorry, time's up")
            temp += 1

    def stop_timer(self):
        # when leaving sit, should store time into string an display on Label
        sit_time = f"{self.hrEntry.get()}:{self.miEntry.get()}:{self.secEntry.get()}"
        curr_time = time.localtime() #datetime.now()
        # must read file and then append new time
        # with open("sat_time.txt") as satFile:
        # 
        date_n_time = _date.replace("/", "-") + " " + time.strftime("%H:%M",curr_time)
        stopped = [date_n_time,sit_time]
        self.write_info(stopped)
        # print(stopped)

        self.init_values()
        self.submit(self.got_time)
        print("stop button pressed")

    def write_info(self,new_data):
        """with open(filename,"r") as inFile:
            data = csv.reader(inFile,delimiter=',')
            for row in data:
                print(row)"""
            
        with open(filename,'a',newline='') as outFile:
            add_data = csv.writer(outFile,delimiter=',')
            add_data.writerow(new_data)


def run_popUp(param):
    # Annoying popUp
    subprocess.run(["stand_up.bat",param])

   
def plot_data(parent):
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    figure = Figure(figsize=(6,4),dpi=100)

    figure_canvas = FigureCanvasTkAgg(figure,master=parent)
    # NavigationToolbar2Tk(figure_canvas)
    axes = figure.add_subplot()#layout='constrained'
    df = pd.read_csv(filename,parse_dates=['date'])
    # Parsing time from string type to dateTime type:
    # pd.to_datetime(df['sitting_time'],format="%H:%M:%S")
    # actually the above added date=1900,01,01 to each time
    # the following works cuz splits string and calcs time in minutes
    df['sit_mins'] = df['sitting_time'].str.split(':').apply(lambda x:int(x[0])*60+int(x[1])+int(x[2])/60)
    # axes.bar(df['date'],df['sit_mins'])
    axes.scatter(df['date'],df['sit_mins'],marker='^')
    axes.xaxis.set_major_locator(locator)
    axes.xaxis.set_major_formatter(formatter)
    figure_canvas.draw()

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=1)

def create_window():
    newWindow = tk.Toplevel()
    return newWindow

if __name__ == "__main__":
    print("Please do NOT close this window")
    app = SittingApp()
    app.mainloop()

   
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