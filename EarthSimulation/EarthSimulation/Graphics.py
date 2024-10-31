from cgi import test
from tkinter import *
from turtle import bgcolor, color
from wsgiref.handlers import BaseCGIHandler
from Earth import Earth
from functools import partial
import matplotlib.pyplot as plt

# graphics for the simulation
class Graphics:
    def __init__(self, rows, columns, pixels, earth):
        self.earth = earth # Earth class object
        self.pixels = pixels
        self.riseInTempAvg = 0
        self.yesterdayRiseInTempAvg = 0
        
        self.ROWS = rows
        self.COLUMNS = columns
        
        self.window = Tk(className = 'Earth Simulator')
        self.window.geometry(str(pixels) + 'x' + str(pixels))
        
        self.frames = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        self.buttons = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        
        self.daysPassed = 0
        self.daysPassedLabel = Label(text = "Days passed: " + str(self.daysPassed), font=('Times New Roman', 15, 'bold'))
        self.infoLabel = Label(text = "", font=('Times New Roman', 15, 'bold'))
        
        self.dayButton = Button(self.window, text = "1 Day",command = self.day)
        self.weekButton = Button(self.window, text = "7 Days",command = self.week)
        self.monthButton = Button(self.window, text = "30 Days",command = self.month)
        self.yearButton = Button(self.window, text = "365 Days",command = self.year)
        self.pltButton = Button(self.window, text = "Temperature average graph", command = self.openPlt)
        
        plt.title("Average temperature change over time")
        plt.xlabel("Days passed")
        plt.ylabel("Average temperature change")
        plt.plot([self.daysPassed, self.riseInTempAvg], [0, 0])
        
        self.initializeWindow()
        self.window.mainloop()
     
    # initializes and opens a graphic representation of earth
    def initializeWindow(self):
        cellColor = " "
        cellType = " "
        
        for i in range(self.ROWS):
            self.window.rowconfigure(i)
            
        for i in range(self.COLUMNS):
            self.window.columnconfigure(i)
            
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                cellType = self.earth.earth[i][j].cellType
                if(cellType == "land"):
                    cellColor = "burlywood1"
                    
                elif(cellType == "sea"):
                    cellColor = "aqua"
                    
                elif(cellType == "iceberg"):
                    cellColor = "cadetblue"
                    
                elif(cellType == "forest"):
                    cellColor = "forestgreen"
                    
                elif(cellType == "city"):
                    cellColor = "grey"
                    
                self.frames[i][j] = Frame(self.window,bg = cellColor, width = self.pixels/self.COLUMNS, height = self.pixels/self.ROWS).grid(row = i, column = j)
                self.buttons[i][j] = Button(text = self.earth.earth[i][j].cellType, bg = cellColor, command=partial(self.printInfo, i, j))
                self.buttons[i][j].grid(row = i, column = j)
                
        self.dayButton.place(x = 500, y = 0)
        self.weekButton.place(x = 500, y = 25)
        self.monthButton.place(x = 500, y = 50)
        self.yearButton.place(x = 500, y = 75)
        self.daysPassedLabel.place(x = 875, y = 0)
        self.infoLabel.place(x = 800, y = 25)
        self.pltButton.place(x = 500, y = 100)
        
    # one step on earth
    def step(self):
        self.infoLabel.config(text = "")
        self.earth.step()
        self.daysPassed += 1
        self.yesterdayRiseInTempAvg = self.riseInTempAvg
        self.riseInTempAvg = self.earth.riseInTempAvg
        plt.plot([self.daysPassed - 1,self.daysPassed], [self.yesterdayRiseInTempAvg, self.riseInTempAvg])
      
    # 1 day on earth
    def day(self):
       self.step()
       self.daysPassedLabel.config(text = "After " + str(self.daysPassed) + " days")
       
    # 7 days on earth
    def week(self):
        for i in range(7):
            self.step()
            
        self.daysPassedLabel.config(text = "After " + str(self.daysPassed) + " days")
       
    # 30 days on earth
    def month(self):
        for i in range(30):
            self.step()
            
        self.daysPassedLabel.config(text = "After " + str(self.daysPassed) + " days")
      
    # 365 days on earth
    def year(self):
        for i in range(365):
            self.step()
            
        self.daysPassedLabel.config(text = "After " + str(self.daysPassed) + " days")
      
    # print the info of a given cell
    def printInfo(self, i, j):
        self.infoLabel.config(text = self.earth.earth[i][j].toString())
   
    # opens the plot of the average temperature change
    def openPlt(self):
        plt.title("Average temperature change over time")
        plt.xlabel("Days passed")
        plt.ylabel("Average temperature change")
        plt.show()
