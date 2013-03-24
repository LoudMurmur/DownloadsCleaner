'''
Created on 24 mars 2013

@author: Eildosa

delete all unwanted files (rar, par, .1, .idx, etc)
rename file with a tag ex : [1080p-Web]
move file from unrecognised folder to a common location
delete empty folders

Do not rename files when resolution is not available in file-name

Used for sabNzbs completed folder.

recognized resolution :
480p (if contains hdtv and no other resolution then it's also 480p)
560p, 720p, 1080p

recognized quality
hdtv, web, dvdrip, bluray, bdrip

'''


from os import listdir
from os.path import isfile, join
import os
import shutil

#global variables !

bad_extensions = { ".exe", ".nfo", ".sfv", ".srr", ".par2", ".jpg", ".html",
                  ".nzb", ".txt", ".1", ".rar", ".srs", ".sub", ".idx"}

good_folders = {"Adventure Time With Finn and Jake", "American Horror Story", 
                "Breaking Bad", "Community", "Continuum",  "Dexter", 
                "Doctor Who", "Fringe", "Game of Thrones", "Grimm", 
                "How I Met Your Mother", "Misfits",  "Mythbusters",
                "Person of Interest", "Sherlock", "Spartacus",
                "Spartacus Blood and Sand", "Supernatural", "The Big Bang Theory",
                "The Mentalist", "The Neighbors", "The Walking Dead", "True Blood"
                }

#Must not be terminated by \ or /
download_folder = "F:\Nouveau dossier"

bad_file_trash = os.path.join(download_folder, "AAA.BAD.FILES")
wrong_folder_trash = os.path.join(download_folder, "AAA.WRONG.FOLDER")
sample_trash = os.path.join(download_folder, "AAA.SAMPLES")

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

def move_to_badfile_trash(file_name_with_path):
    if not os.path.exists(bad_file_trash):
        os.makedirs(bad_file_trash)
    shutil.move(file_name_with_path, bad_file_trash)

def move_to_sample_trash(file_name_with_path):
    if not os.path.exists(sample_trash):
        os.makedirs(sample_trash)
    shutil.move(file_name_with_path, sample_trash)

def move_to_need_manual_sorting(file_name_with_path):
    if not os.path.exists(wrong_folder_trash):
        os.makedirs(wrong_folder_trash)
    shutil.move(file_name_with_path, wrong_folder_trash)

def delete_folder(folder_with_path):
    print "ERASING : "+folder_with_path
    shutil.rmtree(folder_with_path)

def delete_file(file_path):
    """should not be used
    """
    pass

def determine_if_bad_file(file_name_with_path):
    """Return true if file extension is in the list
    (true = file needs to be deleted)
    """
    extension = os.path.splitext(file_name_with_path)
    for be in bad_extensions:
        if extension[1] == be:
            return True
    return False

def determine_if_is_in_good_folder(file_name_with_path):
    """Return true if the file is in a good folder
    if the file is not in a good folder it should be moved
    to the manual sorting area
    """
    for gf in good_folders:
        if file_name_with_path.lower().find(gf.lower()) != -1:
            return True
    return False

def determine_resolution(file_name_with_path, quality):
    """Return the file resolution, if resolution does not appear in the filename
    and quality is hdtv then it is probably 480p"""
    file_without_path = os.path.split(file_name_with_path)[1]
    if file_without_path.lower().find("1080") != -1:
        return "1080p"
    if file_without_path.lower().find("720") != -1:
        return "720p"
    if file_without_path.lower().find("560") != -1:
        return "560p"
    if file_without_path.lower().find("480") != -1:
        return "480p"
    if quality == "hdtv":
        return "480p"
    return "unknown"

def determine_quality(file_name_with_path):
    """Return the file quality"""
    file_without_path = os.path.split(file_name_with_path)[1]
    if file_without_path.lower().find("web") != -1:
        return "web"
    if file_without_path.lower().find("bdrip") != -1:
        return "bdrip"
    if file_without_path.lower().find("dvdrip") != -1:
        return "dvdrip"
    if file_without_path.lower().find("hdrip") != -1:
        return "hdrip"
    if file_without_path.lower().find("hdtv") != -1:
        return "hdtv"
    return "unknown"
    
def determine_tag(file_name_with_path):
    quality = determine_quality(file_name_with_path)
    resolution = determine_resolution(file_name_with_path, quality)
    return ("["+resolution+"-"+quality+"]")

def determine_if_file_is_already_tagged(file_name_with_path):
    """Return True if file already contains a tag ([resolution-quality])"""
    file_name_without_path = os.path.split(file_name_with_path)[1]
    if file_name_without_path.find("[") == 0:
        return True
    return False

def is_folder_empty(folder_path):
    """Return true if the folder is empty
    (empty folders needs to be removed)
    """
    onlyFiles = [ f for f in listdir(folder_path) if isfile(join(folder_path,f)) ]
    onlyDirs = [ f for f in listdir(folder_path) if not isfile(join(folder_path,f)) ]
    
    if len(onlyFiles) == 0:
        if len(onlyDirs) == 0:
            return True
    return False

def remove_all_empty_folders(my_path):
    folder_list = get_all_folders_from(my_path)
    for folder in folder_list:
        remove_all_empty_folders(join(my_path, folder))
        if is_folder_empty(join(my_path, folder)):
            delete_folder(join(my_path, folder))

def ignore_folder_present_in_path(my_path):
    if my_path.lower().find(bad_file_trash.lower()) != -1:
        return True
    if my_path.lower().find(wrong_folder_trash.lower()) != -1:
        return True
    if my_path.lower().find(sample_trash.lower()) != -1:
        return True
    return False






                        ##########################################
                        ##########################################
                        ##########################################
         #              #######                            #######
         #              ####### THIS IS THE ACTUAL PROGRAM #######
         #              #######                            #######
       #####            ##########################################
        ###             ##########################################
         #              ##########################################

#1 Moving bad file to trash
complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
for file_name_with_path in complete_file_list:
    if not ignore_folder_present_in_path(file_name_with_path):
        if determine_if_bad_file(file_name_with_path):
            print "Sending %s to bad file trash" %os.path.split(file_name_with_path)[1]
            move_to_badfile_trash(file_name_with_path)

#2 Moving file in bad folder to manual sorting location
complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
for file_name_with_path in complete_file_list:
    if not ignore_folder_present_in_path(file_name_with_path):
        if not determine_if_is_in_good_folder(file_name_with_path):
            print "Sending %s to manual sorting area" %os.path.split(file_name_with_path)[1]
            move_to_need_manual_sorting(file_name_with_path)

#3 Moving sample to sample location
    #needs to be done
    
#4 tagging files
complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
for file_name_with_path in complete_file_list:
    if not ignore_folder_present_in_path(file_name_with_path):
        if not determine_if_file_is_already_tagged(file_name_with_path):
            tag = determine_tag(file_name_with_path)
            file_name_splitted = os.path.split(file_name_with_path)
            print "renaming %s to %s%s%s" %(file_name_with_path, file_name_splitted[0],tag, file_name_splitted[1])
            os.rename(file_name_with_path, join(file_name_splitted[0], tag+file_name_splitted[1]))
        
#5 Deleting unwanted resolution
    #needs to be done
    
#6 Removing empty folders            
remove_all_empty_folders(download_folder)
            
