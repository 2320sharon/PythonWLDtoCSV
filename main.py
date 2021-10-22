# Python WLD to CSV Converter
#@Author Sharon Fitzpatrick

# Description: Converts WLD files to CSV files
# ------------------------------------------------------
import pandas as pd
import csv
from skimage.io import imread
import xml.etree.ElementTree as ET

# read_wld(wld_file_path)
# Returns a float list containing [XCellSize,YCellSize,UpperleftX,UpperleftY] 
# @Params (wld_file_path)
#     wld_file_path: string representing the path to the .wld file
def read_wld(wld_file_path):
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

#def get_coords(wld_array,rows,cols)
# Returns the xMin, xMax, yMin, yMax of the jpg
# @Params (wld_array,rows,cols)
#     wld_array: float list containing [XCellSize,YCellSize,UpperleftX,UpperleftY]
#     rows: number of rows in jpg
#     cols: number of cols in jpg
def get_coords(wld_array,rows,cols):
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


#def read_xml(xml_path)
# Returns  (["WGS 84 / UTM zone 18N"]) extracted from dataAxisToSRSAxisMapping in the XML
# @Params (xml_path)
#     xml_path: string representing the path to the XML file

def read_xml(xml_path):
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

def create_file_list(path_to_jpgs):
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

def read_jpg(jpg_path):
   # Extract image name from path
   jpg_name=jpg_path.split('\\')[-1];
   print(jpg_name)
   return jpg_name


# def convert_to_list(xmin, xmax, ymin, ymax,crs_string)
# Returns list containing the following data
# image filename,
# Easting min (XMin),
# Easting max (XMax),
# Northing min (YMin),
# Norhting max (YMax),
# Coordinate Reference System (e.g. wgs 84 / utm zone 18N).

# @Params (jpg_name,xmin, xmax, ymin, ymax,crs_string)

def convert_to_list(jpg_name,xmin, xmax, ymin, ymax,crs_string):
       return [jpg_name,xmin,xmax,ymin,ymax,crs_string]
      
# def write_csv(xmin, xmax, ymin, ymax,crs_string)
# Returns true on successful write
# Write line to csv file
# image filename,
# Easting min (XMin),
# Easting max (XMax),
# Northing min (YMin),
# Norhting max (YMax),
# Coordinate Reference System (e.g. wgs 84 / utm zone 18N).
# # 
# @Params (xml_path)
#     xml_path: string representing the path to the XML file     
def write_csv(data,csvfile):
   try:
      with open(csvfile, mode='w') as sample_csv:
         csv_writer = csv.writer(sample_csv, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
         csv_writer.writerow(data)
   except:
      print("Error occured")
      # Find out what kind of error this can throw
      #stop program and trigger a popup




wld_file_path ='PythonWLDtoCSV\sampleData\LC08_014035_20200604.wld'
xml_path='PythonWLDtoCSV\sampleData\LC08_014035_20200604.jpg.aux.xml'
jpg_path='PythonWLDtoCSV\sampleData\LC08_014035_20200604.jpg'

wld_array=read_wld(wld_file_path)
print(wld_array)
rows, cols, bands = imread(jpg_path).shape
xmin, xmax, ymin, ymax = get_coords(wld_array,rows,cols)
print(xmin, xmax, ymin, ymax)

crs_string = read_xml(xml_path)
jpg_name=read_jpg(jpg_path)
data = convert_to_list(jpg_name,xmin, xmax, ymin, ymax,crs_string)
write_csv(data,'sample.csv' )

# Commmand line interface that takes folder containing files and gets them 
# All in one file???
# Check the file types and append them to respective lists
# Once done run the program
# Notify the user when done.

# Allow user to specify the name of the csv

#Specify the location to save csv file to

# Allow user to specifly location to save file in 
# Check if Linux and Windows differ




