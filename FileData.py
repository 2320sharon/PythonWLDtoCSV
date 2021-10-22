from skimage.io import imread
from exceptions import *
import xml.etree.ElementTree as ET

class FileData:
    """A class to hold all data associated with the jpg wld, and xml files."""
    def __init__(self):
         self.WLDPath=""
         self.XMLPath=""
         self.JPGName=""
         self.JPGPath=""

    def setWLDPath(self, wldPath):
        self.WLDPath=wldPath

    def setJPGName(self, JPGName):
        self.JPGName=JPGName

    def setJPGPath(self, JPGpath):
        self.JPGpath=JPGpath

    def setXMLPath(self, XMLPath):
        self.XMLPath=XMLPath

    def getCoords(self,wld_array,rows,cols):
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

    def getWLDArray(self, wldPath):
        """Returns a float list containing [XCellSize,YCellSize,UpperleftX,UpperleftY] 

        Args:
            self: instance variable
            wldPath: string representing the path to the .wld file
                    
        Returns:
            If successful: returns a dictionary containing data from the npz file.

        Raises:
            NPZCorruptException: An error occurred while reading the npz file.

            IOError: An error occured while trying to load the npz file as a pickle
            """
        # empty list to hold file contents as strings
        wld_array=[]
        with open(wldPath) as f:
            wld_array = f.readlines()
            # Remove both rotations
            wld_array.pop(1)
            wld_array.pop(1)
            #Convert Strings to float
            for i,val in enumerate(wld_array):
                wld_array[i] = float(wld_array[i])        
            return wld_array

    def getXmlString(xml_path):
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

    def convert_to_list(self,jpg_name,xmin, xmax, ymin, ymax,crs_string):
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
    
    def createList(self):
        """createList : returns an array containing returns array containing jpg filename, Easting min (XMin), Easting max (XMax), Northing min (YMin),
            Northing max (YMax), Coordinate Reference System (e.g. wgs 84 / utm zone 18N)

        Raises:
            UltimateException:  Raises if WLDPath does not exist
            UltimateException: Raises if XMLPath does not exist
            UltimateException: Raises if JPGpath or does not exist
            UltimateException: Raises if some other error occurs

        Returns:
            array: returns array containing jpg filename, Easting min (XMin), Easting max (XMax), Northing min (YMin),
            Norhting max (YMax), Coordinate Reference System (e.g. wgs 84 / utm zone 18N).
        """
        if self.WLDPath != "" or  self.XMLPath !="" or  self.JPGpath !="" or  self.JPGName !="":
            rows, cols, bands = imread(self.JPGpath).shape
            wldArray = self.getWLDArray(self.WLDPath)
            xmin, xmax, ymin, ymax = self.getCoords(wldArray,rows,cols)
            print(xmin, xmax, ymin, ymax)

            CRSstring=self.getXmlString(self.XMLPath)
            data = self.convert_to_list(self.JPGName,xmin, xmax, ymin, ymax, CRSstring)
            return data
        elif self.WLDPath == "":
            raise UltimateException("Missing data from the .wld file")
        elif self.XMLPath == "":
            raise UltimateException("Missing data from the xml file")
        elif self.JPGpath == "" or self.JPGName !="":
            raise UltimateException("Missing data from the jpg file")
        else:
            raise UltimateException("ERROR: Something happened while reading the files.")