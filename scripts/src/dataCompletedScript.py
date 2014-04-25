'''
Script used by Datamover to query whether a given folder is ready for transfer.
The script returns 0 if the folder is ready for transfer, 1 otherwise.

Created on 31.08.2012

@author: Aaron Ponti

'''

import os
import sys


# Get all files and folders contained in a given directory and optionally
# sub-directories up to a certain level 
def walklevel(currentDir, level = 1):
    currentDir = currentDir.rstrip(os.path.sep)
    assert os.path.isdir(currentDir)
    nSeparators = currentDir.count(os.path.sep)
    for root, dirs, files in os.walk(currentDir):
        yield root, dirs, files
        currentNumSeparators = root.count(os.path.sep)
        if nSeparators + level <= currentNumSeparators:
            del dirs[:]

# Checks that the first level contains only directories and returns the
# list of subfolders
def getFirstLevelSubfolder(currentDir):

    for root, subFolders, files in walklevel(currentDir, 1):
        if len(files) > 0:
            msg = "No files can be present at the root level.\n"
            sys.stderr.write(msg)
            sys.exit(1)

        return subFolders

# ==============================================================================
#
# Program entry point
#
# ==============================================================================

if __name__=="__main__":

    # Check the number of input parameters
    if len(sys.argv) < 2:
        name = os.path.basename(sys.argv[0])
        indx = name.rfind(".")
        if (not indx == -1):
            name = name[:indx]
        msg = "Usage: " + name + " <folder>\n"
        sys.stderr.write(msg)
        sys.exit(1)

    # We do not set up a dedicated logger, since Datamover will redirect all 
    # outputs to standard out and error to the log/datamover_log.txt file
    
    # Get the directory name
    rootDir = sys.argv[1]
    
    # Make sure it is a directory
    if os.path.isdir(rootDir) == False:
        sys.stderr.write("Invalid directory!\n")
        sys.exit(1)

    # RATIONALE
    #
    # The passed folder contains only one subfolder, which is the user subfolder.
    # This contains all the data. To make sure that all data has been annotated,
    # we check for the existence of data_structure.ois and then check that the
    # property files referenced in it do exist at the expected locations. 
    # If any of these tests fail, the folder is not ready to be transferred
    # and the script exits with code 1. Otherwise, the script exits with code 0,
    # which signals Datamover that the whole <rootDir> is ready to be transferred.

    # Get the sub-folders at root level
    subFolders = getFirstLevelSubfolder(rootDir)
    
    # Make sure we have exactly one subfolder
    if len(subFolders) == 0:
        msg = "The folder \"" + rootDir + "\" is empty!\n"
        sys.stderr.write(msg)
        sys.exit(1)

    if len(subFolders) > 1:
        msg = "The folder \"" + rootDir + "\" must contain exactly one subfolder!\n"
        sys.stderr.write(msg)
        sys.exit(1)

    # User folder
    userFolder = subFolders[0]

    # Check whether the data_structure file exists
    dataFileName = os.path.join(rootDir, userFolder, "data_structure.ois")
    if not os.path.exists(dataFileName):
        msg = "File data_structure.ois not found!\n"
        sys.stderr.write(msg)
        sys.exit(1)

    # Read the data structure file and extract all property file names
    # to be checked for existence
    content = None
    with open(dataFileName) as f:
        content = f.readlines()
    f.close()

    # Check that all referenced property files exist
    for line in content:
        # Build file name
        fileName = os.path.join(rootDir, line).rstrip('\n')
        # Check for existence
        if not os.path.exists(fileName):
            msg = "Property file \"" + fileName + "\" not found!\n"
            sys.stderr.write(msg)
            sys.exit(1)

    # We can signal success
    msg = "The folder \"" + rootDir + "\" is ready to be transferred!\n"
    sys.stdout.write(msg)
    sys.exit(0)
