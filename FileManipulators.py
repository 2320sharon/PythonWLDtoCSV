from datetime import datetime
import os
import pathlib
import FileData 
import exceptions
import csv
from csv import writer

# TODO updates the docstring
def createDestinationCSVFile(destinationPath):
    """"Creates a csv file in the in a folder called destination_files
        
    Creates a csv file in the current working directory in a folder called \"destination_files\".
        
    Args:
        None.

    Returns:
        A pathlib.Path containing the exact location of the .csv file within the folder called destination_files
        For example:
            For a windows machine:
                C:\programs\npz_to_csv_converter\destination_files\npz_data_03-Sep-2021_07_47_48.csv
    Raises:
        None.
        """
    timestampStr = datetime.now().strftime("%d-%b-%Y_%H_%M_%S")
    dest_file="CSVData"+timestampStr+".csv"
    destination_path=destinationPath.joinpath(dest_file)
    return destination_path

def delete_empty_file(path_name,logger):
    """"Deletes any empty json files generated.
        
    Checks for empty csv files in the specified path_name of size 0 (AKA empty). If it finds one it deletes it.
        
    Args:
        path_name: A pathlib.Path containing the path to folder containing empty json files.
        logger:    A logger used for debugging.

    Returns:
        None.

    Raises:
        None.
        """
    if os.path.exists(path_name) and os.stat(path_name).st_size == 0:
        logger.debug("Empty file found. Deleting now.")
        os.remove(path_name)

def checkFolderExists(path_name,foldername):
    """"Checks if the specified foldername is a directory within the location specified by pathname
        
    Searches the directory specified by path_name and checks if the foldername is a directory.
        
    Args:
        path_name: A pathlib.Path containing the path to folder
        foldername: A string that contains the name of the folder that is being checked.

    Returns:
        True: If a directory called foldername exists in the path_name provided
        False: If a directory does not exist in the path_name provided

    Raises:
        None.
        """
    for entry in os.scandir(path_name):          
        if entry.is_dir() and entry.name == f"{foldername}":
                return True
    return False
 
def createDestinationFolder(logger):
    """" Creates a directory called destination_files within the current working directory if one does not currently exist.
    Args:
        logger: A logger used for debugging.
    Returns:
        pathlib.Path: containing the location of directory called destination_files within the current working directory 
    Raises:
        None.
        """
    if not checkFolderExists(pathlib.Path.cwd(),"destination_files"):
        logger.debug("\n The directory destination_files is missing and will be created.")
        os.mkdir("destination_files")
    
    return pathlib.Path.cwd().joinpath('destination_files')

def getExtension(file):
    # returns only the extension of the file and check for xml extensions
     fileName,extension = file.split(".",1) # split the file once
     if extension.endswith(".xml"):
        extension="xml"
     return extension

def getFileName(file):
    # returns only the filename
     fileName,extension = file.split(".",1) # split the file once
     return fileName

def openResult(logger,destinationPath):
    """"Opens the directory specifed by destination path    
    Args:
        logger: A logger used for debugging.
    Returns:
        None.
    Raises:
        None.
        """
    if os.name != 'posix':
        os.startfile(destinationPath, 'open')
    else:
        destinationPath='xdg-open '+str(destinationPath)
        os.system( destinationPath)

def writeCSV(data,csvfile):
    """write_csv Writes the data in the array data to a valid csv file 

    Args:
        data (array): array containing the jpg name, xmin, xmax, ymin, ymax, and the CRS string 
        csvfile (pathlib.path): path to the csvfile

    Raises:
         csv.Error: if there is an error writing to the csv file this is raised
    """
    try:
      with open(csvfile, mode='a',newline='') as sample_csv:
         csv_writer = csv.writer(sample_csv, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
         csv_writer.writerow(data)
    except csv.Error as error:
            raise ValueError(error)

def getListofFiles(filesList):
    newFilesArray=[]
    skipFlag=0
    for index,file in enumerate(filesList):
        fileName = getFileName(file)
        print("fileName ", fileName , "index: ", index, "fullname",file )
        if(skipFlag == 1 or skipFlag == 2 ):
            skipFlag=skipFlag-1  #skip processing the next two files that are known matches
            continue
        elif( index+1 >= len(filesList) or index+2 >= len(filesList)):
            break   #No more files left in the array
        elif(fileName == getFileName(filesList[index+1]) and fileName == getFileName(filesList[index+2])):
           skipFlag=2    #Skip the next two files
           miniarray=[]
           miniarray.append(file)
           miniarray.append(filesList[index+1])
           miniarray.append(filesList[index+2])
           newFilesArray.append(miniarray)  #append to the main list of files
        else:       #if next two fileNames do not match it means we cannot process them
            raise exceptions.UltimateException("Error processing files")
        
    return newFilesArray