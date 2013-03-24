'''
Created on 24 mars 2013

@author: thongvan


remove tags from files tagged by donwloadCleaner
'''

from os import listdir
from os.path import isfile, join
import os

download_folder = "F:\Nouveau dossier"

def get_all_files_from(my_path):
    file_list_without_path = [ f for f in listdir(my_path) if isfile(join(my_path,f)) ]
    return file_list_without_path

def get_all_folders_from(my_path):
    folder_list_without_path = [ f for f in listdir(my_path) if not isfile(join(my_path,f)) ]
    return folder_list_without_path

def get_all_files_from_folder_and_sub_folders(my_path):
    """return all file in my_path root and sub-directories
    Not just file names but their path too.
    
    exemple: C:\sabNzbs.completed\truc\Season 1\blabla.avi
    """
    #getting file from this dorectory
    file_list = get_all_files_from(my_path)
    sub_folder_list = get_all_folders_from(my_path)
    
    for i, _file_name in enumerate(file_list):
        file_list[i] = join(my_path,file_list[i])
    
    for folder_name in sub_folder_list:
        return_list = get_all_files_from_folder_and_sub_folders(join(my_path,folder_name))
        file_list.extend(return_list)
    return file_list

def compute_tag_length(file_without_path):
    tag_start = file_without_path.lower().find("[")
    if tag_start == -1:
        return None
    else:
        tag_end = file_without_path.lower().find("]")
        tag_end += 1
        if file_without_path[tag_end] == " ":
            tag_end += 1
        return tag_end
    
def remove_tag(file_with_path, tag_length):
    file_path = os.path.split(file_with_path)[0]
    file_without_path = os.path.split(file_with_path)[1]
    print "%s renamed to\n%s" %(file_without_path, file_without_path[tag_length:])
    os.rename(file_with_path, join(file_path, file_without_path[tag_length:]))


#Actual program

file_list_with_path = get_all_files_from_folder_and_sub_folders(download_folder)
for file_with_path in file_list_with_path:
    file_without_path = os.path.split(file_with_path)[1]
    tag_length = compute_tag_length(file_without_path)
    if tag_length != None:
        remove_tag(file_with_path, tag_length)


