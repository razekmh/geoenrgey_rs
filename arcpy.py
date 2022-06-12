import arcpy
from arcpy.ia import *
from pathlib import Path
import time
import datetime

# output folder
output_folder = Path("E:\Angola\hillshade")
input_folder = Path("E:\Angola\ALOS_DEM")

# set env
arcpy.env.workspace = "E:\Angola\hillshade"

def list_folders(folder):
    list_of_folders = []
    for i in folder.iterdir():
        if i.is_dir():
            list_of_folders.append(i)
    return list_of_folders

def list_dem_files(folder):
    list_dem_files = []
    for i in folder.iterdir():
        if ".dem" in i.suffixes:
            list_dem_files.append(i)
    return list_dem_files

def get_hillshade(dem):
    for angle in [180,225,270,315]:
        out_hillshade_raster = Hillshade(str(dem), angle, 45, 1)
        out_hillshade_raster.save(str(output_folder)+"\\"+Path(dem.stem).stem+"_"+str(angle)+".tif")

dem_folders = list_folders(input_folder)
folder_counter = 0
total_processing_time = 0 
for dem_folder in dem_folders:
    folder_start_time = start = time.time()
    dem_files = list_dem_files(dem_folder)
    for dem_file in dem_files:
        get_hillshade(dem_file)
    folder_counter += 1
    end = time.time()
    folder_processing_time = end - start
    total_processing_time += folder_processing_time

    print(f"{folder_counter} out of {len(dem_folders)} took {folder_processing_time} seconds")
    print(f"avg time = {total_processing_time/folder_counter} seconds, estimated remining time {datetime.timedelta((total_processing_time/folder_counter)*(len(dem_folders)-folder_counter))})