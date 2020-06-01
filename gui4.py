from XML_Einleser import ReadToArray
from UDM_Einleser import UDM_EinleserB
from DataCombiner import Data_Combiner
from UDM_Manipulator import UDMwriter

# GUI imports
import os
import tkinter as tk
from tkinter.filedialog import asksaveasfile, askopenfilename
# end GUI imports


class XmlGUI:

    def __init__(self):
        self.pressureFileName = ''
        self.temperatureFileName = ''
        self.weldFileName = ''
        self.weldSurfaceMovementFileName = ''
        self.fillFileName = ''
        self.udmFileName = ''
        self.saveFileName = ''

        # von Johannes eingefuegt
        self.PartGrade = "Partgrade not Evaluated yet"
        # Bis hierhin

        self.einlesenResult = None
        self.einlesenSucess = None

        self.weldLineGraderResult = None

        self.saveResult = None

        #GUI Buttons and Labels
        self.pressureButton = None
        self.temperatureButton = None
        self.weldButton = None
        self.weldSurfaceButton = None
        self.fillButton = None
        self.udmButton = None

    ### Begin Button Functions ###
    #writing all filenames in their variables
    def loadOnClick(self, filePurpose):
        fileName = askopenfilename(title='Select a {} File'.format(filePurpose))
        if filePurpose == "Pressure":
            # Von Johannes Modifiziert
            self.einlesenSucess.set("Pressure File choosen")
            self.pressureFileName = fileName
            self.pressureButton["text"] = os.path.relpath(fileName,'')
            if ".xml" not in fileName:
                errmsg = "Wrong Pressure File Choosen"
                self.einlesenSucess.set(errmsg)
                self.pressureButton["text"] = "not an xml file..."
            #     bis hierhinn
            print(fileName)
        elif filePurpose == "Temperature":
            self.temperatureFileName = fileName
            self.temperatureButton["text"] = os.path.relpath(fileName,'')
        elif filePurpose == "Weld":
            self.weldFileName = fileName
            self.weldButton["text"] = os.path.relpath(fileName,'')
        elif filePurpose == "Surface":
            self.weldSurfaceMovementFileName = fileName
            self.weldSurfaceButton["text"] = os.path.relpath(fileName,'')
        elif filePurpose == "Fill":
            self.fillFileName = fileName
            self.fillButton["text"] = os.path.relpath(fileName,'')
        elif filePurpose == "UDM":
            self.udmFileName = fileName
            self.udmButton["text"] = os.path.relpath(fileName,'')

    #Run Grader Button
    def einlesenOnClick(self):
        a = self.pressureFileName
        b = self.temperatureFileName
        c = self.weldFileName
        d = self.fillFileName
        e = self.weldSurfaceMovementFileName
        f = self.udmFileName

        Nodes = UDM_EinleserB(f)
        Narr = Nodes.NodesAuslesen()
        Layer = Nodes.Layernamen()

        Readin = ReadToArray(a, b, c, d, e)
        Parr, Tarr, Warr, WSarr, Farr = Readin.einlesen()
        WAA = Readin.getWeldlines(Warr)

        ValuePart, WAA = Readin.getWeldlineGrade(WAA, Parr, Tarr, Farr)
        #NoAr, WeAr,  Va
        combi = Data_Combiner(Narr, WAA, ValuePart)
        Data = combi.Arraysauslesen
        self.einlesenSucess.set(round(ValuePart))
        #non finnished UDM-Manipulator
        #wrt = UDMwriter(Data)
        #wrt.write()
        return

    #dummie
    def weldOnClick(self):
        self.WeldLineGrader()

    #not finnished jet
    #returns error message
    def saveOnClick(self):
        files = [('All Files', '*.*'),
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]

        saveFile = asksaveasfile(filetypes=files, defaultextension=files)
        print(saveFile.name)
        self.saveFileName = saveFile.name
        # TODO using the self.saveFileName, which is the path to the file being saved write the file.
        #  OR if the variable saveFile in a format you can write to, use that to write the data out.
        self.saveResult.set("saving file to {}".format(self.saveFileName))

    ### End Button Functions ###

    #Button Run Weldline Grader(dummie)
    def WeldLineGrader(self):
        if self.einlesenResult == None:
            errMsg = "ERROR: Einlesen result is None, either it hasn't been executed or there was an error when it ran."
            print(errMsg)
            self.weldLineGraderResult.set(errMsg)
            return
        print(self.einlesenResult)
        self.weldLineGraderResult.set(str(self.einlesenResult))

    def runGUI(self):
        # initialize window
        window = tk.Tk()
        window.title("GUI 2.0")
        window.geometry('725x300')

        LABEL_WIDTH = 25
        LABEL_HEIGHT = 15

        WRAPLENGTH = 150

        BUTTON_HEIGHT = 2
        BUTTON_WIDTH = 25

        # add widgets

        ### Begin Load ###
        loadFrame = tk.Frame(
            window,
            height=LABEL_HEIGHT,
            width=LABEL_WIDTH,
        )
        loadFrame.grid(column=1, row=0)

        self.pressureButton = tk.Button(
            loadFrame,
            text="Load Pressure.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Pressure")
        )
        self.pressureButton.grid(column=1, row=0)

        self.temperatureButton = tk.Button(
            loadFrame,
            text="Load Temperature.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Temperature")
        )
        self.temperatureButton.grid(column=1, row=1)

        self.weldButton = tk.Button(
            loadFrame,
            text="Load WeldLines.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Weld")
        )
        self.weldButton.grid(column=1, row=2)

        self.weldSurfaceButton = tk.Button(
            loadFrame,
            text="Load SurfaceMovement.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Surface")
        )
        self.weldSurfaceButton.grid(column=1, row=3)

        self.fillButton = tk.Button(
            loadFrame,
            text="Load FillTime.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Fill")
        )
        self.fillButton.grid(column=1, row=4)

        self.udmButton = tk.Button(
            loadFrame,
            text="Load .udm File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("UDM")
        )
        self.udmButton.grid(column=1, row=5)

        ### End load ###

        ### Begin Einlesen ###
        self.einlesenSucess = tk.StringVar(window)
        #print(self.einlesenSucess)
        self.einlesenSucess.set(self.PartGrade)

        self.weldLineGraderResult = tk.StringVar(window)
        self.weldLineGraderResult.set("Not Executed Yet")

        self.saveResult = tk.StringVar(window)
        self.saveResult.set("Click Button to save a File")

        einlesenLable = tk.Label(
            window,
            textvariable=self.einlesenSucess,
            wraplength=WRAPLENGTH,
            justify=tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            borderwidth=2,
            relief="sunken",
        )

        einlesenLable.grid(column=2, row=0)

        einlesenButton = tk.Button(
            window,
            text="Run Grader",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.einlesenOnClick
        )

        einlesenButton.grid(column=2, row=1)

        ### End Criterion ###

        ### Begin Weldline ###

        wildlineLable = tk.Label(
            window,
            textvariable=self.weldLineGraderResult,
            wraplength=WRAPLENGTH,
            justify=tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            borderwidth=2,
            relief="sunken",
        )

        wildlineLable.grid(column=3, row=0)

        wildlineButton = tk.Button(
            window,
            text="Run Weld Line Grader",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.weldOnClick
        )

        wildlineButton.grid(column=3, row=1)

        ### End Wildline ###

        ### Begin Save ###

        saveLable = tk.Label(
            window,
            textvariable=self.saveResult,
            wraplength=WRAPLENGTH,
            justify=tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
        )

        saveLable.grid(column=4, row=0)

        saveButton = tk.Button(
            window,
            text="Save File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.saveOnClick #dummie
        )

        saveButton.grid(column=4, row=1)

        ### End Save ###

        # build/display window with the attached widgets
        window.mainloop()