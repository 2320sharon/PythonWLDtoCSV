# Python WLD to CSV Converter
#@Author Sharon Fitzpatrick

# Description: Converts WLD files to CSV files
# ------------------------------------------------------
import tkinter as tk
from WLDtoCSVClass import *
import FileManipulators
from tkinter import filedialog, messagebox, ttk
from FileData import *

class InstructionFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent,background=parent.frame_color)
        self.__create_widgets(parent)
    
    def __create_widgets(self,parent):
        label_title =  tk.Label(self, text="\n.WLD to CSV converter\n")
        label_title.config( foreground= "white",background=parent.frame_color)
        label_title.grid(row=0,column=2,pady=5)

        label_instructions = tk.Label(self, text="Instructions:\n1. Select the folder where the .wld, xml, and jpg files are located by using the \"Select Folder\" button.\n All the files that are related to each other must have the same file name.\n2. Click the \"Run\" button to convert the files to csv.\n3. Click \"Select Folder to Store Results\" to see your resulting csv file. ")
        label_instructions.config( foreground= "white",background=parent.frame_color)
        label_instructions.grid(row=0,column=2,pady=5)
        
class MainApp(tk.Tk):

     #Defining App colors
    # ---------------------------------
    background_color ='#121212'
    frame_color='#292929'
    text_color='#6C6C6C'
    button_purple="#6200B3"
    #----------------------------------

    #                                                   DIALOG BOXES
    #-----------------------------------------------------------------------------------------------------------------------
    def ErrorBox(self,msg):
        """" A system error dialog box that informs the user an recoverable error has occured and the program will quit. 
        Args:
            self: An instance of the MainApp class
            msg: A custom msg provided by the program that typically specifies what kind of error occured.
        Returns:
            None
        Raises:
            None
        """
        messagebox.showerror(title='ERROR', message=f"{msg}")
    
    def ErrorMsgBbox(self,msg):
        """" A system error dialog box that informs the user an recoverable error has occured and the program will quit. 
        Args:
            self: An instance of the MainApp class
            msg: A custom msg provided by the program that typically specifies what kind of error occured.
        Returns:
            None
        Raises:
            None
        """
        messagebox.showerror(title='ERROR', message=f"{msg}\nThere has been an unrecoverable error.\nExiting now")
        self.quit()

    def EmptySourceMsgBox(self,npz_path):
        """" A system error dialog box that asks the user to choose a directory to open .npz files with or quits the program
        
            If the user selects yes and chooses to select a directory to read .npz files from the open_file_dialog()
            will be executed. If the user selects option no then the program exits.
        Args:
            self: An instance of the MainApp class
            npz_path: a pathlib.path to the current directory where .npz files would be read from
        Returns:
            Exits the program if the user choose not to select a directory with .npz files
        Raises:
            None
        """
        MsgBox = messagebox.askquestion (title=f"Would you like to add some .npz files?",message=f"You don\'t have any npz files at the location:\n {npz_path}.\n Would you like to add some .npz files?",icon = 'warning')
        if MsgBox == 'yes':
            self.OpenFileDialog()
        else:
            messagebox.showerror(title='Exit', message=f"There are no npz files in {npz_path} directory.\nExiting now")
            self.quit()

    def InvalidMsgBox(self,filename):
        """" A system error dialog box that informs the user an error occured while attempting to read the filename
        
        Args:
            self: An instance of the MainApp class.
            filename: A string specifying the file name that could not be processed.
        Returns:
            None
        Raises:
            None
        """
        messagebox.showerror(title='Exit', message=f"{filename} was not a valid file and was skipped.")

    def SuccessMsgBox(self,filename):
        """" A system info dialog box that informs the user a csv file was successfully created.
        
        Args:
            self: An instance of the MainApp class.
            filename: A string specifying the file name that was generated.
        Returns:
            None
        Raises:
            None
        """
        messagebox.showinfo(title='Success', message=f"{filename} was generated",icon='info')
    #                                                   End of DIALOG BOXES
    #-----------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        tk.Tk.__init__(self,className=" .WLD to CSV converter")
        #make sure the destination folder exists to store the resulting JSON file
        self.wait_visibility()
        #create the main app's gui
        self.build_main_app()
        #make the subframes within the main app
        self.__create_frames()

        self.Left_Frame=tk.Frame(self,pady=10,padx=10,background=MainApp.frame_color)
        self.Left_Frame.pack(side='left',padx=10,pady=10)

        #Frame to hold the "Select Folder" button and the corresponding labels
        #-----------------------------------------------------------------
        self.folder_frame=tk.Frame(self.Left_Frame,height = 75,width = 120,pady=10,padx=10,background=MainApp.frame_color)
        self.folder_frame.pack(side='top',padx=5,pady=5)

        #pathSourcePathlabel labels the path containing the source directory exists. Empty by default
        self.pathSourcePathlabel=tk.Label(self.folder_frame, text="",wraplength=220, justify="center")
        self.pathSourcePathlabel.config( foreground= "white",background=MainApp.frame_color)
        self.pathSourcePathlabel.grid(row=1,column=0)

        #label_folder_instr labels the location above where the path containing the source directory exists
        self.label_folder_instr=tk.Label(self.folder_frame,text="Directory containing xml,wld,jpg files:")
        self.label_folder_instr.config( foreground= "white",background=MainApp.frame_color)
        self.label_folder_instr.grid(row=0,column=0)

        #Button to open a folder
        self.Open_Folder_button = tk.Button(self.folder_frame, text="Select Folder", command= lambda: self.OpenFileDialog(True),background=MainApp.button_purple,fg="white")
        self.Open_Folder_button.grid(row=2,column=0,pady=10,padx=5)
        #-------------------------------------------------------------------

        #Frame to hold the "Select Folder to hold Results" button and the corresponding labels
        #-----------------------------------------------------------------
        self.folder_destination_frame=tk.Frame(self.Left_Frame,height = 50,width = 100,pady=5,padx=5,background=MainApp.frame_color)
        self.folder_destination_frame.pack(side='bottom',padx=5,pady=5)

        #pathDestinationPathlabel labels the path containing the destination directory exists. Empty by default
        self.pathDestinationPathlabel=tk.Label(self.folder_destination_frame, text="",wraplength=220, justify="center")
        self.pathDestinationPathlabel.config( foreground= "white",background=MainApp.frame_color)
        self.pathDestinationPathlabel.grid(row=1,column=0)

        #path_label instructions for path to results 
        self.label_folder_destination_instr=tk.Label(self.folder_destination_frame,text="Directory to store results:")
        self.label_folder_destination_instr.config( foreground= "white",background=MainApp.frame_color)
        self.label_folder_destination_instr.grid(row=0,column=0)

        #Button to open a folder
        #  self.Open_Folder_button = tk.Button(self.folder_destination_frame, text="Select Folder to Store Results", command= lambda: self.open_file_dialog(self.label_folder_destination_instr),background=MainApp.button_purple,fg="white")
        self.Open_Folder_button = tk.Button(self.folder_destination_frame, text="Select Folder to Store Results", command= lambda: self.OpenFileDialog(False),background=MainApp.button_purple,fg="white")
        self.Open_Folder_button.grid(row=2,column=0,pady=5,padx=5)
        #-------------------------------------------------------------------

        # Frames to hold listbox and associated components
        # ---------------------------------------------------------
        #Create frame to hold scrolling list and buttons to change list
        self.list_holder=tk.Frame(self,width=150,height = 210,background=MainApp.frame_color,padx=7,pady=7)
        self.list_holder.pack(side='right',pady=10,padx=5)

        #Create a frame to hold the list
        self.list_frame=tk.Frame(self.list_holder,height = 500,width = 250,pady=10)
        self.xlist_scroll_bar=tk.Scrollbar(self.list_frame, orient='horizontal')
        self.ylist_scroll_bar=tk.Scrollbar(self.list_frame, orient='vertical')

        delete_all_button=tk.Button(self.list_holder,text="Clear All",command=self.deleteAll_listbox,background=MainApp.button_purple,fg="white")
        delete_all_button.grid(column=0,row = 2,pady=5,padx=10)

        #Create the listbox to hold the files in the directory to read xml,wld,jpg files from
        self.filesListbox=tk.Listbox(self.list_frame,width=50,yscrollcommand=self.ylist_scroll_bar.set,xscrollcommand=self.xlist_scroll_bar.set,bg=MainApp.background_color,fg="white",highlightbackground="#EA7AF4",selectbackground="#EA7AF4",activestyle='none')

        #Configure the scrollbar to scroll within the list vertically and horizontally
        self.ylist_scroll_bar.config(command=self.filesListbox.yview)
        self.xlist_scroll_bar.config(command=self.filesListbox.xview)
        #1. Pack the scrollbar within the listframe
        self.xlist_scroll_bar.pack(side='bottom',fill='x')
        #2. Pack the frame 
        self.list_frame.grid(column=2,row=1,padx=5,pady=5)
        #3.Place the list within the frame
        self.filesListbox.pack(side='left')
        #4.Place the vertical scrollbar after the horizontal one
        self.ylist_scroll_bar.pack(side='right',fill='y')
        # -----------------------------------------------------------------------------------------------------------------

        #Create a frame to hold all the buttons related to opening and creating the results
        self.ResultButtonsFrame=tk.Frame(self,width=150,height = 150,background=MainApp.frame_color,padx=7,pady=7)
        self.ResultButtonsFrame.pack(side='bottom',pady=10,padx=5)

        self.button_run = tk.Button(self.ResultButtonsFrame,text="Run", command=self.ConvertCSV,background=MainApp.button_purple,fg="white")
        self.button_run.pack(side='top')

        self.button_result = tk.Button(self.ResultButtonsFrame, text="Open CSV",command=lambda:self.chooseDestination(), background=MainApp.button_purple,fg="white")
        self.button_result.pack(side='bottom',pady=10)

    def build_main_app(self):
        """"Builds the main frame of the app.
        Builds the main frame of the app by specifiying the dimensions of the app, the background colors, the transparency, and
        where on the user's screen it will display.
        Note: This may cause errors on user's who have multiple displays.
        Args:
             self: An instance of the MainApp class.
        Returns:
           None.
        Raises:
            None.
        """
        window_width = 830
        window_height = 420
        # get the screen dimension
        screen_width =  self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(window_width,window_height)
        self['background']=MainApp.background_color
        self.attributes('-alpha',0.97)          #makes the GUI transparent

    def __create_frames(self):
        """"Creates independent sub frames to be nested within the main frame.
        Creates the instrucution frame and packs it into the main frame.
        Args:
             self: An instance of the MainApp class.
        Returns:
           None.
        Raises:
            None.
        """
        self.instructionframe=InstructionFrame(self)
        self.instructionframe.pack(side='top')

    def deleteAll_listbox(self):
        """"Deletes all items from the listbox"""
        self.filesListbox.delete(0,'end')

    def readListbox(self):
        """"Reads all items in the listbox.
       Gets the size of the listbox then reads all the items from the listbox and returns them as a list.
        Args:
             self: An instance of the MainApp class.
        Returns:
           A list containing all the files in the listbox.
        Raises:
           None.
        """       
        list_size=self.filesListbox.size()
        npztuple =self.filesListbox.get(0,list_size-1)
        npzlist=list(npztuple)
        return npzlist

    def checkValidFileType(self,file):
        # Returns true if the given file is of type , jpg, wld, or xml if it does not returns false
        if file.lower().endswith('.jpg') or file.lower().endswith('.wld') or file.lower().endswith('.xml'):
            return True
        else:
            return False

    def create_file_list(self,filesPath):
        #Function to convert all the items in the path to a list containing only files
        #OS MAY HAVE ISSUES WITH LINUX AND MAC
        if os.path.exists(filesPath):                #ensure the path exists before attempting to access the directory
            files_list=os.listdir(filesPath)
            if files_list != []:                    #Ensure it is not an empty directory
                validFilesList = [file for file in files_list if self.checkValidFileType(file) and os.path.isfile(os.path.join(filesPath, file))]
                return validFilesList 
            else:
                self.EmptySourceMsgBox(filesPath)
                return []
        else:
            self.ErrorMsgBbox(msg=f"ERROR\nThe folder {filesPath} does not exist.\n")
            return []

    def createValidFilesList(self,filesList):
        """createValidFilesList: Returns a list of all the files that had three matching filenames and each file was of type: jpg,xml,wld.
    
        Creates two lists,badFilesList and goodFilesList, which will hold the list of all the bad and good files respectiveally. A file is considered good
        if it has two matching files with the same file name an of types jpg,xml,wld. The list of goodfiles is returned.
        A file is bad if it does not have two matching files with the same filename and of types jpg,xml,wld.
        
        Args:
            filesList (array): list of all the files within the source directory

        Returns:
            array: a list of all the files that had three matching filenames and each file was of type: jpg,xml,wld.
        """
        # ALL POSSIBLE FILE TYPES
        FILE_TYPES=['.jpg','.wld','.xml']
        # Copy of file types that can be manipulated
        currentFileTypes=FILE_TYPES.copy()
        skipFlag=0
        # sort files list by filenames
        filesList.sort()
        badFilesList=[]
        goodFilesList=[]
        for index,file in enumerate(filesList):

            fileName,extension = os.path.splitext(f"{file}")
            if(skipFlag == 1 or skipFlag == 2 ):
                skipFlag=skipFlag-1  #skip processing the next two files that are known matches
                goodFilesList.append(file)
                continue
            elif( index+1 >= len(filesList) or index+2 >= len(filesList)):
                badFilesList.append(file)   #no more files in list after this
                if(index+1 < len(filesList)):
                     badFilesList.append(filesList[index+1])  #no more files in list after this
                break
            # elif((fileName.find(FileManipulators.getFileName(filesList[index+1])) or FileManipulators.getFileName(filesList[index+1]).find(fileName)) and (fileName.find(FileManipulators.getFileName(filesList[index+2])) or FileManipulators.getFileName(filesList[index+2]).find(fileName))):
            elif(fileName.replace(".jpg.aux","") == FileManipulators.getFileName(filesList[index+1]).replace(".jpg.aux","") and fileName.replace(".jpg.aux","") == FileManipulators.getFileName(filesList[index+2]).replace(".jpg.aux","")):      
                extension1=FileManipulators.getExtension(filesList[index+1])
                currentFileTypes.remove(extension)
                if(extension1 in currentFileTypes):
                    currentFileTypes.remove(extension1)
                extension2=FileManipulators.getExtension(filesList[index+2])
                if(extension2 in currentFileTypes):
                    skipFlag=2
                    goodFilesList.append(file)
                else:
                    badFilesList.append(file)
                currentFileTypes=FILE_TYPES.copy() #reset the fileTypes array for the next compatsion
            else:       #if next two fileNames do not match it means we cannot process them
                badFilesList.append(file)

        if badFilesList != []:
            badFilePath=FileManipulators.create_badFile_file()
            with open(badFilePath, 'a') as writer:
                for file in badFilesList:
                    writer.write(file+"\n")
            self.ErrorBox(f"A list of invalid files have been written to: ${badFilePath}")
        return goodFilesList

    def populateFilesList(self, filePath):
         #Update the list box
        filesList=self.create_file_list(filePath)
        validFilesList=self.createValidFilesList(filesList)

        #delete everything from listbox first to ensure clean insert
        self.deleteAll_listbox()
        #insert all the files into the listbox
        for item in  validFilesList:
            self.filesListbox.insert('end',item)

    def getSourcePath(self):
        """getSourcePath returns the path to the source directory specifed by the user

        Raises:
            EmptySourcePath: raises if the path to source files is invalid

        Returns:
           [Pathlib.path]: path to source folder where jpg,wld,xml
        """
        sourcePath = self.pathSourcePathlabel.cget("text")
        if sourcePath == "":
           raise EmptySourcePath
        else:
            return Path(sourcePath)

    def OpenFileDialog(self, isSourceLocation):
        """"Prompts the user to specify a directory where the files are located. Then saves the absolute path to a label and inserts all
        the files into the listbox if isSourceLocation = true, otherwise it update the pathDestinationPathlabel to contain the path to the directory 
        where the resulting csv file will be stored. 

       Prompts the user to specify a directory where the files are located using a system file box. Then saves the absolute path to either the source
       or destination path label. If the path is for the source directory then it calls a function to populate the listbox, if the path is for destination 
       then it only updates the destination label.
        Args:
             self: An instance of the MainApp class.
             isSourceLocation: A boolean value that if true true means that filepath is the location of the source files
                              if false it means filepath is the location of the destination where the csv will be stored
        Returns:
          None.
        Raises:
           None.
        """    
        filePath=filedialog.askdirectory(mustexist=True,initialdir= '/',title='Please select a directory')
        # If isSourceLocation is true: filePath is the location of the directory containing the source files to process
        if isSourceLocation: 
            self.pathSourcePathlabel.config( text=f"{filePath}")
            self.populateFilesList(filePath)
        else: 
            self.pathDestinationPathlabel.config( text=f"{filePath}")

    def getDestinationPath(self):
        """getDestinationPath returns a path to where the csv will be created depending on user input
        Returns:
            [Pathlib.path]: path to destination folder where csv file be stored
        """
        destinationPath = self.pathDestinationPathlabel.cget("text")
        if destinationPath == "":
            return FileManipulators.createDestinationFolder()
        else:
            return Path(destinationPath)

    def chooseDestination(self):
        destinationPath=self.getDestinationPath()
        FileManipulators.openResult(destinationPath)

    def processFiles(self,sourcePath,ArrayoffilesList,destinationPath):
        """processFiles inserts all the valid files from the listbox into the csv file at the location specified by destinationPath

        Args:
            sourcePath (pathlib.path): path to where source files are located
            ArrayoffilesList (array of arrays): an array containing arrays which contain files of the same name with each of the file types xml,jpg,wld
            destinationPath (pathlib.path): path to where the csv file is located
        """
        # successfulWrite boolean flag to indicate if a write to the csv file has occured
        successfulWrite=False
        for filesArray in ArrayoffilesList:
            fileDataObject=FileData()           #Create an object to hold all the file data
            for index,file in enumerate(filesArray):
                if(file.endswith('xml')):
                    # Join sourcePath with the xml file name
                    fullXMLPath=sourcePath.joinpath(file)
                    fileDataObject.setXMLPath(fullXMLPath)
                if(file.endswith('jpg')):
                     fileDataObject.setJPGName(file)
                     # Join sourcePath with the jpg file name
                     fullJPGPath=sourcePath.joinpath(file)
                     fileDataObject.setJPGPath(fullJPGPath)
                if(file.endswith('wld')):
                     # Join sourcePath with the jpg file name
                     fullWLDPath=sourcePath.joinpath(file)
                     fileDataObject.setWLDPath(fullWLDPath)
                if(index == 2):     #this is the last spot in the subarray of matching filenames
                    try:
                        data=fileDataObject.createList()
                        FileManipulators.writeCSV(data,destinationPath)
                        successfulWrite=True
                    except ValueError as err :
                        self.InvalidMsgBox(f"Error writing to the file: {destinationPath}")
                    except UltimateException as err:
                        self.InvalidMsgBox(err)
                   
        
        #At the end check if at least one set of .wld,.jpg,.xml file was converted to CSV successfully.
        if successfulWrite:
            self.SuccessMsgBox(destinationPath)

    def ConvertCSV(self):
        """"Creates a csv file from the files in the listbox.
       
       Runs all the necessary functions to create a csv file. It starts by verifiying the destination files directory exists.
       It then gets the absolute path to the directory containing the files. It gets the list of the file name from the listbox.
       It then reads all the files and creates a csv file. It then checks if the csv file generated is empty and if it is then it deletes
       it.
        Args:
             self: An instance of the MainApp class.
        Returns:
          None.
        Raises:
           None.
        """
        destinationPath=self.getDestinationPath()
        try:
            sourcePath=self.getSourcePath()
        except  EmptySourcePath as emptySourcePathError:
            self.ErrorMsgBbox( emptySourcePathError.msg)
        filesList=self.readListbox()        #valid files from the listbox.
        ArrayoffilesList=FileManipulators.getListofFiles(filesList) 
        # Create the CSV files in the destination location
        CSVFile=FileManipulators.createDestinationCSVFile(destinationPath)

        self.processFiles(sourcePath,ArrayoffilesList,CSVFile)
        FileManipulators.delete_empty_file(CSVFile)

if __name__ == "__main__":
    #Runs App
    app=MainApp()
    app.mainloop()