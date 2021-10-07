# Python WLD to CSV Converter
#@Author Sharon Fitzpatrick

# Description: Converts WLD files to CSV files
# ------------------------------------------------------

# PseudoCode
import pandas as pd
from skimage.io import imread
import xml.etree.ElementTree as ET

# read_wld()
# Returns a float list containing [XCellSize,YCellSize,UpperleftX,UpperleftY] 
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
# Returns the xmin, xmax, ymin, ymax of the jpg
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

def read_xml(xml_path):
   tree = ET.parse(xml_path)
   root = tree.getroot()
   print(root)
   dataAxisToSRSAxisMapping=''
   # print(root.attrib)
   for child in root:
      print(child.tag, child.attrib,child.text)
      if child.tag == 'SRS':
         dataAxisToSRSAxisMapping=child.text
   
   print(dataAxisToSRSAxisMapping)
   #  return xml_info


# def parse_crs():
#    (do stuff)
#    return crs_string
# crs_string = parse_crs(xml_info)


# xml_info = read_xml(xml_file)
wld_file_path ='PythonWLDtoCSV\sampleData\LC08_014035_20200604.wld'
xml_path='PythonWLDtoCSV\sampleData\LC08_014035_20200604.jpg.aux.xml'
wld_array=read_wld(wld_file_path)
print(wld_array)
rows, cols, bands = imread('PythonWLDtoCSV\sampleData\LC08_014035_20200604.jpg').shape
xmin, xmax, ymin, ymax = get_coords(wld_array,rows,cols)
print(xmin, xmax, ymin, ymax)
read_xml(xml_path)



# def write_csv():
#    (do stuff)
# write_csv(xmin, xmax, ymin, ymax,crs_string )

