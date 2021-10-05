# Python WLD to CSV Converter
#@Author Sharon Fitzpatrick

# Description: Converts WLD files to CSV files
# ------------------------------------------------------

# PseudoCode
import pandas as pd
from skimage.io import imread
def read_xml():
   (do stuff)
    return xml_info

def read_wld():
   (do stuff)
    return wld_info

xml_info = read_xml(xml_file)
wld_info = read_xml(wld_file)
rows, cols, bands = imread(jpeg_file).shape

def get_coords():
   (do stuff)
    return xmin, xmax, ymin, ymax
xmin, xmax, ymin, ymax = get_coords(worldx, xcellsize, worldy, ycellsize, cols, rows)

def parse_crs():
   (do stuff)
   return crs_string
crs_string = parse_crs(xml_info)

def write_csv():
   (do stuff)
write_csv(xmin, xmax, ymin, ymax,crs_string )

