from pci.link import link
from pci.line import line
from pci.fexport import fexport
import pci
from pathlib import Path
# from pci.fimport import fimport
import time
import datetime


input_folder = Path(r"F:\Angola\from_DEM_ALOS_PALSAR")
output_folder = Path(r"F:\Angola\Lineament_from_DEM")
successful_files_log = Path(str(output_folder) + "\\successful_files_log.txt")
failed_files_log = Path(str(output_folder) + "\\failed_files_log.txt")
processed_files_log = Path(str(output_folder) + "\\processed_files_log.txt")

def check_processed_files(list_tif_files):
    processed_files_list = []
    filtered_tif_files_list = []
    if processed_files_log.exists():
        with open(str(processed_files_log),"r") as processed_files_log_text:
            processed_files_list = processed_files_log_text.readlines()
            processed_files_list = [processed_file.strip("\n") for processed_file in processed_files_list]
            for tif_file in list_tif_files:
                if tif_file.name in processed_files_list:
                    print(tif_file)
                else:
                    filtered_tif_files_list.append(tif_file)
                    # print(tif_file.name)
                    # print(processed_files_list)
    return filtered_tif_files_list
    #         print([tif_file for tif_file in list_tif_files if tif_file.name in processed_files_list] )
    # return [tif_file for tif_file in list_tif_files if tif_file.name not in processed_files_list]    

def list_folders(folder):
    list_of_folders = []
    for i in folder.iterdir():
        if i.is_dir():
            list_of_folders.append(i)
    return list_of_folders

def list_tif_files(folder):
    list_tif_files = []
    for i in folder.iterdir():
        if ".tif" in i.suffixes and len(i.suffixes) == 1:
            list_tif_files.append(i)
    return check_processed_files(list_tif_files)

def write_file_in_log(log_file, tif_file):
    with open(str(log_file),"a") as log_file_text:
        log_file_text.write(str(tif_file.name) + "\n")


file_counter = 0
total_processing_time = 0 

def get_lineamnet(shade_file):
        print("Processing file "+str(shade_file))
        tif_file = str(shade_file)
        pix_file = str(output_folder/shade_file.stem)+"_tif"+".pix"
        shp_file = str(output_folder/shade_file.stem)+".shp"
        link(fili=tif_file, filo=pix_file)
        line(fili=pix_file, filo=pix_file, dbic=[1])
        fexport(fili=pix_file, filo=shp_file, dbvs=[2], ftype="shp")

failed_tif = []
list_of_tif_files = list_tif_files(input_folder)
for tif_file in list_of_tif_files:
    file_start_time = start = time.time()
    try:
        get_lineamnet(tif_file)
        write_file_in_log(successful_files_log, tif_file)
        print("file "+ str(tif_file) + " added to successful")
    except pci.exceptions.ParameterException as e:
        failed_tif.append((tif_file,e))
        write_file_in_log(failed_files_log, tif_file)
        print("file "+ str(tif_file) + " added to failed")
    write_file_in_log(processed_files_log, tif_file)
    file_counter += 1
    end = time.time()
    file_processing_time = end - start
    total_processing_time += file_processing_time
    print(str(file_counter)+" out of "+str(len(list_of_tif_files))+" took "+str(file_processing_time)+" seconds")
    print("avg time = "+str(total_processing_time/file_counter)+" seconds, estimated remining time "+str(datetime.timedelta(seconds=(total_processing_time/file_counter)*(len(list_of_tif_files)-file_counter))))

print(failed_tif)