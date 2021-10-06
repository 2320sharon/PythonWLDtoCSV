# Python WLD to CSV Converter
#@Author Sharon Fitzpatrick

# Description: Converts WLD files to CSV files
# ------------------------------------------------------

# PseudoCode
import pandas as pd
from skimage.io import imread


# def read_xml():
#    (do stuff)
#     return xml_info

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


# xml_info = read_xml(xml_file)
wld_file_path ='PythonWLDtoCSV\sampleData\LC08_014035_20200604.wld'
wld_array=read_wld(wld_file_path)
print(wld_array)
# wld_info = read_xml(wld_file)
# rows, cols, bands = imread(jpeg_file).shape

# def get_coords():
   # XMin = WorldX - (XCellSize / 2)
   # YMax = WorldY - (YCellSize / 2)
   # XMax = (WorldX + (Cols * XCellSize)) - (XCellSize / 2)
   # YMin = (WorldY + (Rows * YCellSize)) - (YCellSize / 2)
#     return xmin, xmax, ymin, ymax
# xmin, xmax, ymin, ymax = get_coords(worldx, xcellsize, worldy, ycellsize, cols, rows)

# def parse_crs():
#    (do stuff)
#    return crs_string
# crs_string = parse_crs(xml_info)

# def write_csv():
#    (do stuff)
# write_csv(xmin, xmax, ymin, ymax,crs_string )

