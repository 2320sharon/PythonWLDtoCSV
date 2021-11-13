from datetime import datetime
import os
import pathlib
import FileData 
import exceptions
import csv
from csv import writer

def create_badFile_file():
    """create_badFile_file 

    Args:
        destinationPath (path):path to where results will be stored

    Returns:
        path: returns path to the newly generated bad file .txt
    """
    timestampStr = datetime.now().strftime("%d-%b-%Y_%H_%M_%S")
    dest_file="BadFiles_"+timestampStr+".txt"
    # if not os.path.exists(pathlib.Path.cwd().joinpath('bad_files')):
    # Check whether the specified path exists or not
    path=pathlib.Path.cwd().joinpath('bad_files')
    if not os.path.exists(path):
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    result_path = path
    destination_path=result_path.joinpath(dest_file)
    return destination_path

def createDestinationCSVFile(destinationPath):
    """"Creates a csv file in the in a folder called destination_files
        
    Creates a csv file in the current working directory in a folder called \"destination_files\".
        
    Args:
        destinationPath: path to the folder where the results are stored

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

def delete_empty_file(path_name,):
    """"Deletes any empty json files generated.
        
    Checks for empty csv files in the specified path_name of size 0 (AKA empty). If it finds one it deletes it.
        
    Args:
        path_name: A pathlib.Path containing the path to folder containing empty json files.

    Returns:
        None.

    Raises:
        None.
        """
    if os.path.exists(path_name) and os.stat(path_name).st_size == 0:
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
 
def createDestinationFolder():
    """" Creates a directory called destination_files within the current working directory if one does not currently exist.
    Returns:
        pathlib.Path: containing the location of directory called destination_files within the current working directory 
    Raises:
        None.
        """
    if not checkFolderExists(pathlib.Path.cwd(),"destination_files"):
        os.mkdir("destination_files")
    
    return pathlib.Path.cwd().joinpath('destination_files')

def getExtension(file):
    # returns only the extension of the file and check for xml extensions
     fileName,extension = os.path.splitext(f"{file}")
     if extension == ".xml":
        extension="xml"
     return extension

def getFileName(file):
    # returns only the filename
     fileName,extension = os.path.splitext(f"{file}")
     return fileName

def openResult(destinationPath):
    """"Opens the directory specifed by destination path    
    Args:

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
        # (fileName.find(getFileName(filesList[index+1])) or getFileName(filesList[index+1]).find(fileName)) and (fileName.find(getFileName(filesList[index+2])) or getFileName(filesList[index+2]).find(fileName))
        # elif(fileName == getFileName(filesList[index+1]) and fileName == getFileName(filesList[index+2])):
        # elif((fileName.find(getFileName(filesList[index+1])) or getFileName(filesList[index+1]).find(fileName)) and (fileName.find(getFileName(filesList[index+2])) or getFileName(filesList[index+2]).find(fileName))):
        elif(fileName.replace(".jpg.aux","") == getFileName(filesList[index+1]).replace(".jpg.aux","") and fileName.replace(".jpg.aux","") == getFileName(filesList[index+2]).replace(".jpg.aux","")):   
           skipFlag=2    #Skip the next two files
           miniarray=[]
           miniarray.append(file)
           miniarray.append(filesList[index+1])
           miniarray.append(filesList[index+2])
           newFilesArray.append(miniarray)  #append to the main list of files
        else:       #if next two fileNames do not match it means we cannot process them
            raise exceptions.UltimateException("Error processing files")
        
    return newFilesArray