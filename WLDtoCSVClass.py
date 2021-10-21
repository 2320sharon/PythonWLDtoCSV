import os as os
import numpy as np
from numpy.lib.npyio import load
import json
import pathlib
from exceptions import *
import logging
from datetime import datetime
from pathlib import Path     #necessary for reading the npz files and writing the final json file
import os
import pandas as pd
import csv
from skimage.io import imread
import xml.etree.ElementTree as ET

#                                               LOG CREATION FUNCTIONS
#-----------------------------------------------------------------------------------------------------------------------
def make_log_file_path():
    """"Creates the absoltute path where the log file will be generated
          
        Uses the current date and time to generate a unique log file.

    Args:
        None.
    Returns:
        A pathlib.Path containing the absolute path to the directory called log_files
        For example:
            For a windows machine:
                C:\programs\npz_to_json_converter\log_files\log_03-Sep-2021_07_47_40.log
    Raises:
        None.
        """
    timestampStr = datetime.now().strftime("%d-%b-%Y_%H_%M_%S")
    file_name="log_"+timestampStr+".log"
    dir_path = Path.cwd().joinpath('log_files')
    print(f"\nLog files location: {dir_path}")
    if not os.path.exists(dir_path):
        print(f"\nLocation does not exist: {dir_path}.\n Creating it now. \n")
        os.mkdir(dir_path)
    log_path=dir_path.joinpath(file_name)
    print(f"\nLog: {log_path} has been created. \n")
    return log_path

def create_filehandler_logger(file_log_name):
    """"Creates the file handler for the logger using the filename
          
    Args:
        None.
    Returns:
        None.
    Raises:
        None.
        """
    file_handler = logging.FileHandler(file_log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

#Creating the logger here
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
#-----------------------------------------------------------------------------------------------------------------------

class WLDtoCSVClass:
    """A class to hold all data associated with the jpg wld, and xml files and contains methods to convert from npz to json.
    """
    # def __init__(self):

    def read_xml(xml_path):
        """read_xml: returns (["WGS 84 / UTM zone 18N"]) extracted from dataAxisToSRSAxisMapping in the XML

        [extended_summary]

        Args:
            xml_path (string): representing the path to the XML file.

        Raises:
            IncorrectFileTypeException: [description]

        Returns:
            string: (["WGS 84 / UTM zone 18N"]) extracted from dataAxisToSRSAxisMapping in the XML
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()
        dataAxisToSRSAxisMapping=''
        for child in root:
            print(child.tag, child.attrib,child.text)
            if child.tag == 'SRS':
                dataAxisToSRSAxisMapping=child.text
        

        # Get this string PROJCS["WGS 84 / UTM zone 18N"
        commaPosition= dataAxisToSRSAxisMapping.find(',');
        #Slice string from PROJCS to first , not inclusive
        dataAxisToSRSAxisMapping= dataAxisToSRSAxisMapping[0:commaPosition]
        PROCJSPosition= dataAxisToSRSAxisMapping.find('S');
        #Remove PROJCS
        dataAxisToSRSAxisMapping= dataAxisToSRSAxisMapping[(PROCJSPosition+1):]
        #add a closing ]
        dataAxisToSRSAxisMapping= dataAxisToSRSAxisMapping+"]"
        print(dataAxisToSRSAxisMapping)
        #GOAL: (["WGS 84 / UTM zone 18N"])
        return  dataAxisToSRSAxisMapping

    def read_jpg(jpg_path):
            # Extract image name from path
            jpg_name=jpg_path.split('\\')[-1];
            print(jpg_name)
            return jpg_name

    def get_coords(wld_array,rows,cols):
        """get_coords Returns the xMin, xMax, yMin, yMax of the jpg

        Args:
            wld_array (float list): containing [XCellSize,YCellSize,UpperleftX,UpperleftY]
            rows (int): number of rows in jpg
            cols (int):  number of columns in jpg

        Returns:
             xMin, xMax, yMin, yMax
        """
        # Get all the variables out of the array
        WorldY=wld_array.pop();
        WorldX=wld_array.pop();
        YCellSize=wld_array.pop();
        XCellSize=wld_array.pop();
        del wld_array

        xMin = WorldX - (XCellSize / 2)
        yMax = WorldY - (YCellSize / 2)
        xMax = (WorldX + (cols * XCellSize)) - (XCellSize / 2)
        yMin = (WorldY + (rows * YCellSize)) - (YCellSize / 2)
        return xMin, xMax, yMin, yMax

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
            logger.error(f"ERROR \n Invalid file type {file_extension} is not allowed! \n File: {self.file_path} is not a valid {fileType} file. \n End of ERROR")
            raise IncorrectFileTypeException(filename=self.file_name)

    def convert_to_list(jpg_name,xmin, xmax, ymin, ymax,crs_string):
        """convert_to_list # Returns list containing the following data
            image filename,
            Easting min (XMin),
            Easting max (XMax),
            Northing min (YMin),
            Norhting max (YMax),
            Coordinate Reference System (e.g. wgs 84 / utm zone 18N).

        Args:
            jpg_name (string): image filename
            xmin (double): Easting min
            xmax (double): Easting max 
            ymin (double): Northing min 
            ymax (double): Northing max 
            crs_string (string): Coordinate Reference System (e.g. wgs 84 / utm zone 18N)

        Returns:
            [type]: [description]
        """
        return [jpg_name,xmin,xmax,ymin,ymax,crs_string]

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

    def write_csv(data,csvfile):
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
    
    #TODO Add exception handling
    #TODO Add exception handling documentation
    def read_wld(self, wld_file_path):
        """Returns a float list containing [XCellSize,YCellSize,UpperleftX,UpperleftY] 

        Args:
            self: instance variable
            wld_file_path: string representing the path to the .wld file
                    
        Returns:
            If successful: returns a dictionary containing data from the npz file.

        Raises:
            NPZCorruptException: An error occurred while reading the npz file.

            IOError: An error occured while trying to load the npz file as a pickle
            """
            # empty list to hold file contents as strings
            wld_array=[]
            with open(wld_file_path) as f:
                wld_array = f.readlines()
                # Remove both rotations
                wld_array.pop(1)
                wld_array.pop(1)
                #Convert Strings to float
                for i,val in enumerate(wld_array):
                    wld_array[i] = float(wld_array[i])

            return wld_array

    
