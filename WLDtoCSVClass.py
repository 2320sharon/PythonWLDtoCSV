import os as os
from numpy.lib.npyio import load
from exceptions import *
from datetime import datetime
from pathlib import Path     #necessary for reading the npz files and writing the final json file
import os
import pandas as pd
import csv
from skimage.io import imread
import xml.etree.ElementTree as ET

class WLDtoCSVClass:
    """A class to hold all data associated with the jpg wld, and xml files and contains methods to convert from npz to json.
    """
    # def __init__(self):

    def check_file(self,fileType):
        """check_file(self): checks if the file given is of type fileType.

            Returns nothing

            Args:
                self: instance variable

            Raises:
                IncorrectFileTypeException: Raises exception when the file is not of type NPZ
        """
        filename,file_extension= os.path.splitext(self.file_name)
        if file_extension != fileType:                                                            #if npz file does not exist throw an exception
            print(f"ERROR \n Invalid file type {file_extension} is not allowed! \n File: {self.file_path} is not a valid {fileType} file. \n End of ERROR")
            raise IncorrectFileTypeException(filename=self.file_name)

    def createDataTuple(self,filepath):
            """createDataTuple returns a tuple containing the matching jpg,xml,wld. If a non matching file is found
            it is added misMatched files list.

            [extended_summary]

            Args:
                filepath ([string]): file path to the folder containing the source files

            Raises:
                UltimateException: [description]

            Returns:
                [mismatchedList]: mismatched files and null is empty
                [array of tuples]:array made of matching tuples
            """

    def writeCSV(self,data,csvfile):
        """write_csv write the content in the array, data, to the corresponding row given by the path of the
        csvfile.

        Args:
            data (list[]): list containing # image filename,Easting min (XMin),Easting max (XMax),Northing min (YMin),
            Northing max (YMax),Coordinate Reference System (e.g. wgs 84 / utm zone 18N).
            csvfile (path): full path to the location of the csv file
        """
        try:
            with open(csvfile, mode='w') as sample_csv:
                csv_writer = csv.writer(sample_csv, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(data)
        except:
            print("Error occured")
            # Find out what kind of error this can throw
            #stop program and trigger a popup

    def create_file_list(path_to_jpgs):
        """create_file_list [summary]

        [extended_summary]

        Args:
            path_to_jpgs ([type]): [description]

        Returns:
            [type]: [description]
        """
        #OS MAY HAVE ISSUES WITH LINUX AND MAC
        if os.path.exists(path_to_jpgs):                #ensure the path exists before attempting to access the directory
            files_list=os.listdir(path_to_jpgs)
            if files_list != []:                    #Ensure it is not an empty directory
                npz_list = [file for file in files_list if file.lower().endswith('.jpg') and os.path.isfile(os.path.join(path_to_jpgs, file))]
                print(npz_list)
                return npz_list 
            else:
                print("empty list")
                return []
        else:
            print("path does not exist")
            return []
    

    
