import xml.etree.ElementTree as ET
import numpy as np

# GUI imports
import tkinter as tk

from tkinter.filedialog import asksaveasfile, askopenfilenames, askopenfilename
#end GUI imports
class XmlGUI:

    def __init__(self):
        super().__init__()
        self.pressureFileName = ''
        self.temperatureFileName = ''
        self.weldFileName = ''
        self.fillFileName = ''
        self.udmFileName = ''

        self.einlesenResult = None
        self.einlesenSucess = None 

        self.weldLineGraderResult = None




    ### Begin Button Functions ###

    def loadOnClick(self,filePurpose):
        fileName = askopenfilename(title='Select a {} File'.format(filePurpose))
        if filePurpose == "Pressure":
            self.pressureFileName = fileName
        elif filePurpose == "Temperature":
            self.temperatureFileName = fileName
        elif filePurpose == "Weld":
            self.weldFileName = fileName
        elif filePurpose == "Fill":
            self.fillFileName = fileName
        elif filePurpose == "Umd":
            self.udmFileName = fileName
        else:
            print("ERROR filePurpose does not match, contact Kendall Despain on Freelancer.com for details")

    def einlesenOnClick(self):

        for i in range(0, 4, 1):
            if i == 0:
                datei = self.pressureFileName
            elif i == 1:
                datei = self.pressureFileName
            elif i == 2:
                datei = self.weldFileName
            else:
                datei = self.fillFileName
            
            if datei == '':
                errMsg = "ERROR: One of the files was not loaded. In interation {}.".format(i)
                print(errMsg)
                self.einlesenSucess.set(errMsg)
                return

            
        self.einlesenSucess.set("Einlesen Suceeded")

        #TODO: I don't know where you are using the udm file, but it's path name is being stored in self.udmFileName
        #TODO: uncomment next line or modify it to pass the correct value into WeldLineGrader
        #self.einlesenResult = WAA

    def weldOnClick(self):
        self.WeldLineGrader()
        
    ### End Button Functions ###
    
    def WeldLineGrader(self):
        if self.einlesenResult == None:
            errMsg = "ERROR: Einlesen result is None, either it hasn't been executed or there was an error when it ran."
            print(errMsg)
            self.weldLineGraderResult.set(errMsg)
            return
        print(self.einlesenResult)
        self.weldLineGraderResult.set(str(self.einlesenResult))

    def runGUI(self):
        #initialize window
        window = tk.Tk()
        window.title("GUI 2.0")
        window.geometry('725x275')

        LABEL_WIDTH = 25
        LABEL_HEIGHT = 15

        WRAPLENGTH = 125

        BUTTON_HEIGHT= 2
        BUTTON_WIDTH = 23

        #add widgets

        ### Begin Load ###
        loadFrame = tk.Frame(
            window,
            height = LABEL_HEIGHT,
            width = LABEL_WIDTH,
        )
        loadFrame.grid(column=1,row=0)

        pressureButton = tk.Button(
            loadFrame,
            text="Load Pressure File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Pressure")
            ) 
        pressureButton.grid(column=1,row=0)

        temperatureButton = tk.Button(
            loadFrame,
            text="Load Temperature File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Temperature")
            ) 
        temperatureButton.grid(column=1,row=1)

        weldButton = tk.Button(
            loadFrame,
            text="Load Weld File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Weld")
            ) 
        weldButton.grid(column=1,row=2)

        fillButton = tk.Button(
            loadFrame,
            text="Load Fill File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Fill")
            ) 
        fillButton.grid(column=1,row=3)

        udmButton = tk.Button(
            loadFrame,
            text="Load Udm File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Umd")
            ) 
        udmButton.grid(column=1,row=4)

        ### End load ###

        ### Begin Einlesen ###
        self.einlesenSucess = tk.StringVar(window)
        self.einlesenSucess.set("Not Executed Yet")

        self.weldLineGraderResult = tk.StringVar(window)
        self.weldLineGraderResult.set("Not Executed Yet")

        einlesenLable= tk.Label(
            window,
            textvariable=self.einlesenSucess,
            wraplength=WRAPLENGTH,
            justify = tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            borderwidth=2,
            relief="sunken",
            )

        einlesenLable.grid(column=2,row=0)

        einlesenButton = tk.Button(
            window,
            text="Run Einlesen",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.einlesenOnClick
            )

        einlesenButton.grid(column=2,row=1)

        ### End Criterion ###

        ### Begin Wildline ###

        wildlineLable= tk.Label(
            window,
            textvariable=self.weldLineGraderResult,
            wraplength=WRAPLENGTH,
            justify = tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            borderwidth=2,
            relief="sunken",
            )

        wildlineLable.grid(column=3,row=0)

        wildlineButton = tk.Button(
            window,
            text="Run Weld Line Grader",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.weldOnClick
            )

        wildlineButton.grid(column=3,row=1)

        ### End Wildline ###

        #build/display window with the attached widgets
        window.mainloop()


# run gui when file is run... ie type python gui3.py
gui = XmlGUI()
gui.runGUI()  