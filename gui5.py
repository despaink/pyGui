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

        self.layerResult = None

        self.saveResult = None

        #GUI Buttons and Labels
        self.pressureButton = None
        self.temperatureButton = None
        self.weldButton = None
        self.weldSurfaceButton = None
        self.fillButton = None
        self.udmButton = None

        self.dropOptionLabel = None
        self.dropOptions = ['_______','Layer 1', 'Layer 2',]

    ### Begin Button Functions ###

    #based on Von Johannes Modifiziert which I liked
    def isCorrectFileType(self, filePurpose, fileName, fileType):
        if fileType not in fileName:
            errmsg = "Wrong {} File Choosen".format(filePurpose)
            self.einlesenResult.set(errmsg)
            return False
        return True


    #writing all filenames in their variables, changes button labels to file names
    def loadOnClick(self, filePurpose):
        fileName = askopenfilename(title='Select a {} File'.format(filePurpose))
        if filePurpose == "Pressure":
            self.pressureFileName = fileName
            self.pressureButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".xml"):
                self.pressureButton["text"] = "Not an xml file."

        elif filePurpose == "Temperature":
            self.temperatureFileName = fileName
            self.temperatureButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".xml"):
                self.temperatureButton["text"] = "Not an xml file."
       
        elif filePurpose == "Weld Line":
            self.weldFileName = fileName
            self.weldButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".xml"):
                self.weldButton["text"] = "Not an xml file."
       
        elif filePurpose == "Weld Surface Movement":
            self.weldSurfaceMovementFileName = fileName
            self.weldSurfaceButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".xml"):
                self.weldSurfaceButton["text"] = "Not an xml file."
       
        elif filePurpose == "Fill":
            self.fillFileName = fileName
            self.fillButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".xml"):
                self.fillButton["text"] = "Not an xml file."
       
        elif filePurpose == "UDM":
            self.udmFileName = fileName
            self.udmButton["text"] = os.path.relpath(fileName,'')

            if not self.isCorrectFileType(filePurpose,fileName,".udm"):
                self.udmButton["text"] = "Not an udm file."

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
        self.einlesenResult.set(round(ValuePart))
        self.einlesenSucess = True
        #non finnished UDM-Manipulator
        #wrt = UDMwriter(Data)
        #wrt.write()
        return

    #dummie
    def onLayerChanged(self, *args):
        layerValue = self.dropOptionLabel.get()

        if layerValue == self.dropOptions[1]:
            self.layerResult.set(self.dropOptions[1])
            #TODO insert non dummie here for layer 1

        elif layerValue == self.dropOptions[2]:
            self.layerResult.set(self.dropOptions[2])
            #TODO insert non dummie here for layer 2
        
        else:
            self.layerResult.set("No Layer Selected")

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
            command=lambda: self.loadOnClick("Weld Line")
        )
        self.weldButton.grid(column=1, row=2)

        self.weldSurfaceButton = tk.Button(
            loadFrame,
            text="Load SurfaceMovement.XML File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=lambda: self.loadOnClick("Weld Surface Movement")
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
        self.einlesenResult = tk.StringVar(window)
        #print(self.einlesenSucess)
        self.einlesenResult.set(self.PartGrade)

        self.layerResult = tk.StringVar(window)
        self.layerResult.set("No Layer Selected")

        self.saveResult = tk.StringVar(window)
        self.saveResult.set("Click Button to save a File")

        einlesenLable = tk.Label(
            window,
            textvariable=self.einlesenResult,
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

        ### End Einlesen ###

        ### Begin dropDown ###

        layerLable = tk.Label(
            window,
            textvariable=self.layerResult,
            wraplength=WRAPLENGTH,
            justify=tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            borderwidth=2,
            relief="sunken",
        )

        layerLable.grid(column=3, row=0)

        self.dropOptionLabel = tk.StringVar(window)
        self.dropOptionLabel.set(self.dropOptions[0])

        dropDown = tk.OptionMenu(
            window,
            self.dropOptionLabel,
            *self.dropOptions
        )

        dropDown.grid(column=3, row=1)

        self.dropOptionLabel.trace('w',self.onLayerChanged)

        ### End dropDown ###

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