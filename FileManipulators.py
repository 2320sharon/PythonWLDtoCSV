from datetime import datetime
import os
import pathlib


def create_destination_file():
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
    dest_file="npz_data_"+timestampStr+".csv"
    result_path = pathlib.Path.cwd().joinpath('destination_files')
    destination_path=result_path.joinpath(dest_file)
    return destination_path

def delete_empty_file(path_name,logger):
    """"Deletes any empty json files generated.
        
    Checks for empty .json files in the specified path_name of size 0 (AKA empty). If it finds one it deletes it.
        
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

def check_folder_exists(path_name,foldername):
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

#TODO modify to check if the user's results folder exists
#TODO pass the destination name to this function
def createDestinationFolder(logger):
    """"Verifies the directory called destination_files exists within the current working directory.
        
    Creates a directory called destination_files within the current working directory if one does not currently exist.
        
    Args:
        logger: A logger used for debugging.

    Returns:
        None.

    Raises:
        None.
        """
    if not check_folder_exists(pathlib.Path.cwd(),"destination_files"):
        logger.debug("\n The directory destination_files is missing and will be created.")
        os.mkdir("destination_files")
    
    return pathlib.Path.cwd().joinpath('destination_files')

def open_result(logger,destinationPath):
    """"Opens the directory called destination_files in a gui interface according the user's PC type.
        
    Verifies the directory called destination_files exists within the current working directory.
        
    Args:
        logger: A logger used for debugging.

    Returns:
        None.

    Raises:
        None.
        """
    # If the destinationPath is blank make the default location in the Program's directory
    print("\n destinationPath",destinationPath)
    if destinationPath == "":
        destPath=createDestinationFolder(logger)
    else:
        destPath=pathlib.Path(destinationPath)

    if os.name != 'posix':
        os.startfile(destPath, 'open')
    else:
        os.system('xdg-open '+os.getcwd()+os.sep+'destination_files')

