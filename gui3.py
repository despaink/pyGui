import xml.etree.ElementTree as ET
import numpy as np

# GUI imports
import tkinter as tk

from tkinter.filedialog import asksaveasfile, askopenfilename
#end GUI imports
class XmlGUI:

    def __init__(self):
        super().__init__()
        self.pressureFileName = ''
        self.temperatureFileName = ''
        self.weldFileName = ''
        self.fillFileName = ''
        self.udmFileName = ''
        self.saveFileName = ''

        self.einlesenResult = None
        self.einlesenSucess = None 

        self.weldLineGraderResult = None

        self.saveResult = None




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
            print("ERROR filePurpose does not match, contact Kendall Despain on Freelancer.com for details or give the above code a good read.")

    def einlesenOnClick(self):
        # Bestimmen der Elementanzahl und speichern dieser im arrcount array für Druck,Temp, Weldline und FillTime

        for i in range(0, 4, 1):
            currentdateiName = ''
            if i == 0:
                datei = self.pressureFileName
                currentdateiName = 'pressure'
            elif i == 1:
                datei = self.temperatureFileName
                currentdateiName = 'temperature'
            elif i == 2:
                datei = self.weldFileName
                currentdateiName = 'weld'
            else:
                datei = self.fillFileName
                currentdateiName = 'fill'
            
            if datei == '':
                errMsg = "ERROR: {} file has not been loaded.".format(currentdateiName)
                print(errMsg)
                self.einlesenSucess.set(errMsg)
                return

            # Creation of File specific Element-tree
            tree = ET.parse(datei)
            root = tree.getroot()
            # Counting of the amount of Node Elements
            count = 0
            for elem in root.iter('NumberOfDependentVariables'):
                ct = elem.text
                cint = int(ct)
                count += cint
        # print(datei, count)

            if i == 0:
                # Set Dimension based on counts
                Parr = np.empty((count, 3), dtype=np.float32)
                # Fill Array with Node ID and value and Timestamp based on xml File
                j = 0

                for elem1 in root.iter('Block'):
                    TimeTag = elem1.find('IndpVar')
                    Time_txt = TimeTag.get('Value')
                    Time = np.float32(Time_txt)
                    # print(elem1.attrib)
                    # print(Time)
                    for elem2 in elem1.iter('NodeData'):
                        Id_in_txt = elem2.get('ID')
                        Value_in_txt = elem2.find('DeptValues').text

                        Id = np.float32(Id_in_txt)
                        Value = np.float32(Value_in_txt)

                        Parr[j, 0] = Id
                        # print(f"Id Druck {Id}")
                        Parr[j, 1] = Value
                        Parr[j, 2] = Time
                        j += 1
            # k = 802
            # print(f"ID {Parr[k, 0]} Value {Parr[k, 1]} Time {Parr[k, 2]}")

            if i == 1:
                # Set Dimension based on counts
                Tarr = np.empty((count, 3), dtype=np.float32)
                # Fill Array with Node ID and value based on xml File
                j = 0

                for elem1 in root.iter('Block'):
                    TimeTag = elem1.find('IndpVar')
                    Time_txt = TimeTag.get('Value')
                    Time = np.float32(Time_txt)
                    # print(elem1.attrib)
                    # print(Time)
                    for elem2 in elem1.iter('NodeData'):
                        Id_in_txt = elem2.get('ID')
                        Value_in_txt = elem2.find('DeptValues').text

                        Id = np.float32(Id_in_txt)
                        Value = np.float32(Value_in_txt)

                        Tarr[j, 0] = Id
                        # print(f"Id Temp {Id}")
                        Tarr[j, 1] = Value
                        Tarr[j, 2] = Time
                        j += 1
            if i == 2:
                # Set Dimension based on counts
                Warr = np.empty((count, 2), dtype=np.float32)
                # Fill Array with Node ID and value based on xml File
                j = 0
                for elem in root.iter('NodeData'):
                    Id_in_txt = elem.get('ID')
                    Value_in_txt = elem.find('DeptValues').text

                    Id = np.float32(Id_in_txt)
                    Value = np.float32(Value_in_txt)

                    Warr[j, 0] = Id
                    Warr[j, 1] = Value
                    j += 1

            if i == 3:
                # Set Dimension based on counts
                Farr = np.empty((count, 2), dtype=np.float32)
                # Fill Array with Node ID and value based on xml File
                j = 0
                for elem in root.iter('NodeData'):
                    Id_in_txt = elem.get('ID')
                    Value_in_txt = elem.find('DeptValues').text

                    Id = np.float32(Id_in_txt)
                    Value = np.float32(Value_in_txt)

                    Farr[j, 0] = Id
                    Farr[j, 1] = Value
                    j += 1
            # print(datei, count)


        # print('Druck ', Parr)
        # print('Temp', Tarr)
        # print('Weldlines ', Warr)
        # print('Filltime ', Farr)



        # The created Arrays will be redesigned to show only Weldline Points

        # Set the Iteration boundaries for the different Arrays
        Warrsize = int((Warr.size/2)-1)
        Farrsize = int((Farr.size/2)-1)
        Parrsize = int((Parr.size / 3) - 1)
        Tarrsize = int((Tarr.size / 3) - 1)

        # Creation of Weldline Arrays
        WAA = np.empty((Warrsize+1, 3), dtype=np.float32)
        WPA = np.empty((Parrsize+1, 3), dtype=np.float32)
        WTA = np.empty((Tarrsize+1, 3), dtype=np.float32)



        # Set Pressure and Temperature Index
        PI = 0
        TI = 0

        # Get the ID of a Weldline Node and look for matching ID in the other Arrays to get the Values
        for k in range(0, Warrsize, 1):
            Id = Warr[k, 0]
            Angle = Warr[k, 1]
            #Get the Filltime of the Node
            for l in range(0, Farrsize, 1):
                Idf = Farr[l, 0]
                if Id == Idf:
                    Filltime = Farr[l, 1]
                    WAA[k, 0] = Id
                    WAA[k, 1] = Filltime
            #Set Pressure and Time in Weldline Pressure Array
            for m in range(0, Parrsize, 1):
                Idp = Parr[m, 0]
                if Id == Idp:
                    Pval = Parr[m, 1]
                    Ptime = Parr[m, 2]
                    WPA[PI, 0] = Id
                    WPA[PI, 1] = Pval
                    WPA[PI, 2] = Ptime
                    # print(f" Id {Id} Druck {Pval} Druckzeit { Ptime}")
                    PI += 1
            # Set Pressure and Time in Weldline Temperature Array
            for n in range(0, Tarrsize, 1):
                IdT = Tarr[n, 0]
                if Id == IdT:
                    Tval = Tarr[n, 1]
                    Ttime = Tarr[n, 2]
                    WTA[TI, 0] = Id
                    WTA[TI, 1] = Tval
                    WTA[TI, 2] = Ttime
                    # print(f" Id {Id} Temp {Tval} Tempzeit {Ttime}")
                    TI += 1


        #//////////////////////////Grading of the Weldline Points



        # Get Injection Temperature:
        # Code goes through all Points where Filltime is zero and gets node ID
        # Where FT Id matches Nodes with Temp Array All Points are respected to find average Node Temp Value
        Temp = 0
        Tcount = 0

        for p in range(0, Farrsize, 1):
            if Farr[p, 1] == 0:
                maxwert = 0
                idf = Farr[p, 0]
                for q in range(0, Tarrsize, 1):
                    if Tarr[q, 0] == idf:
                        tempwert = Tarr[q, 1]
                        if tempwert > maxwert:
                            maxwert = tempwert
                Temp += maxwert
                Tcount += 1
        Taverage = Temp/Tcount
        #print(Taverage)
        

        # Evaluate each Weldline Node by Temperature difference, Pressure gradient, Meeting angle
        WGradeArray = np.empty((WAA.size + 1, 2), dtype=np.float32)
        # Get Node ID for Evalutation

        # for i in range(0, WAA.size+1, 1):
        #     Pgrade = 0
        #     WId = WAA[i, 0]
        #     print(WAA[i, 0] ,WAA[i, 1])
        #     # If Meeting angle bigger then 13 degrees Melt Line
        #     if WAA[i, 1] > 135:
        #         Pgrade += 1







        # for O in range(0, 10, 1):
            # print(f" Id { XMLarr[O, 0]} P { XMLarr[O, 1]}  T { XMLarr[O, 2]} tP { XMLarr[O, 3]} tT { XMLarr[O, 4]} angle { XMLarr[O, 5]} Ft { XMLarr[O, 6]}")
            # diff = XMLarr[O, 3] - XMLarr[O, 4]
            # if diff != 0:
            #    print(f"Diff  {diff} tP {XMLarr[O, 3]}  tT {XMLarr[O, 4]}")
        self.einlesenSucess.set("Einlesen Suceeded TAverage: {}".format(Taverage))

        #TODO: I don't know where you are using the udm file, but it's path name is being stored in self.udmFileName
        #TODO: uncomment next line or modify it to do pass the correct value into WeldLineGrader
        #self.einlesenResult = WAA

    def weldOnClick(self):
        self.WeldLineGrader()

    def saveOnClick(self):
        files = [('All Files', '*.*'),  
                ('Python Files', '*.py'), 
                ('Text Document', '*.txt')]

        saveFile = asksaveasfile(filetypes = files, defaultextension = files)
        print(saveFile.name)
        self.saveFileName = saveFile.name
        #TODO using the self.saveFileName, which is the path to the file being saved write the file.
        #  OR if the variable saveFile in a format you can write to, use that to write the data out. 
        self.saveResult.set("saving file to {}".format(self.saveFileName))

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

        WRAPLENGTH = 150

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

        self.saveResult = tk.StringVar(window)
        self.saveResult.set("Click Button to save a File")

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
            text="Read Files",
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

        ### Begin Save ###

        saveLable= tk.Label(
            window,
            textvariable=self.saveResult,
            wraplength=WRAPLENGTH,
            justify = tk.CENTER,
            width=LABEL_WIDTH,
            height=LABEL_HEIGHT,
            )

        saveLable.grid(column=4,row=0)

        saveButton = tk.Button(
            window,
            text="Save File",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.saveOnClick
            )

        saveButton.grid(column=4,row=1)

        ### End Save ###

        #build/display window with the attached widgets
        window.mainloop() 