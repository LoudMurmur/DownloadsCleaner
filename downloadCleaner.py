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

#set to True and the program will print everything he is doing
DEBUG_MODE = False

bad_extensions = { ".exe", ".nfo", ".sfv", ".srr", ".par2", ".jpg", ".html", ".url",
                  ".nzb", ".txt", ".1", ".rar", ".srs", ".sub", ".idx", ".bat",
                  ".deb", ".sh", ".7z", ".bz2", ".gz", ".r00", ".r01", ".r02", ".r03",
                   ".r04", ".r05", ".r06", ".r07"}

good_folders = {"Adventure Time With Finn and Jake", "American Horror Story", 
                "Breaking Bad", "Community", "Continuum",  "Dexter", 
                "Doctor Who", "Fringe", "Game of Thrones", "Grimm", 
                "How I Met Your Mother", "Misfits",  "Mythbusters",
                "Person of Interest", "Sherlock", "Spartacus",
                "Spartacus Blood and Sand", "Supernatural", "The Big Bang Theory",
                "The Mentalist", "The Neighbors", "The Walking Dead", "True Blood",
                "orphan black", "Doctor Who 2005"
                }

rejected = {" ita ", "xpt-", "epz-", "vostfr", "french", "spanish", "german", 
            ".ita.", "ita-", "-tvp-", "-tvp", "tvp-", " tvp ", ".tvp.", " sof ",
            "-sof", "-sof-", "sof-", ".sof."}


#delete#.480.720.except.web
"""
will delete all 480p resolution in the folder containing the file "delete.480p.720p.except.web"
except 480p and 720p from web source
the except xxx is optional, you can except many resolution by doing
.except.XXX.YYY.EEE

in short :

#delete#.resolution1.resolution2.resolution3.except.quality1.quality2.quality3.etc)
this is called a tagKey
"""

#Must not be terminated by \ or /
download_folder = "F:\SabNzbD.complete"

bad_file_trash = os.path.join(download_folder, "AAA.BAD.FILES")
wrong_folder_trash = os.path.join(download_folder, "AAA.WRONG.FOLDER")
sample_trash = os.path.join(download_folder, "AAA.SAMPLES")
rejected_trash = os.path.join(download_folder, "AAA.REJECTED")
unwanted_trash = os.path.join(download_folder, "AAA.UNWANTED")
duplicate_trash = os.path.join(download_folder, "AAA.DUPLICATE")
icons_folder = os.path.join(download_folder, "#ICONS")

def get_all_files_from(my_path):
    """return all filename in a folder, without their path"""
    file_list_without_path = [ f for f in listdir(my_path) if isfile(join(my_path,f)) and 'desktop.ini' not in f ]
    return file_list_without_path
    
def get_all_folders_from(my_path):
    """ return all folder in a folder without their path"""
    folder_list_without_path = [ f for f in listdir(my_path) if not isfile(join(my_path,f)) ]
    return folder_list_without_path
    
def get_all_files_from_folder_and_sub_folders(my_path):
    """return all file in my_path root and sub-directories
    Not just file names but their path too.
    
    exemple: C:\sabNzbs.completed\truc\Season 1\blabla.avi
    """
    #getting file from this directory
    file_list = get_all_files_from(my_path)
    sub_folder_list = get_all_folders_from(my_path)
    
    for i, _file_name in enumerate(file_list):
        file_list[i] = join(my_path,file_list[i])
    
    for folder_name in sub_folder_list:
        return_list = get_all_files_from_folder_and_sub_folders(join(my_path,folder_name))
        file_list.extend(return_list)
    return file_list

def move_safely_to(destination, file_name_with_path):
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:
        shutil.move(file_name_with_path, destination)
    except shutil.Error:
        i = 0
        file_name_without_path = os.path.split(file_name_with_path)[1]
        while os.path.isfile(join(destination, file_name_without_path+str(i))):
            i += 1
        os.rename(file_name_with_path, join(os.path.split(file_name_with_path)[0], os.path.split(file_name_with_path)[1]+str(i)))    
        shutil.move(file_name_with_path+str(i), destination)

def delete_folder(folder_with_path):
    debug_print("ERASING : "+folder_with_path)
    shutil.rmtree(folder_with_path)

def delete_file(file_path):
    """should not be used, too dangerous.
    in case of algorythm error you could loose
    a lot of stuff, move to a trash folder and check
    yourself if it really needs to be deleted
    """
    pass

def bad_file(file_name_with_path):
    """Return true if file extension is in the list
    (true = file needs to be deleted)
    """
    extension = os.path.splitext(file_name_with_path)
    for be in bad_extensions:
        if extension[1] == be:
            return True
    return False

def is_in_good_folder(file_name_with_path):
    """Return true if the file is in a good folder
    if the file is not in a good folder it should be moved
    to the manual sorting area
    """
    for gf in good_folders:
        #print "comparing : %s and %s" %(os.path.split(file_name_with_path)[0].lower(), gf.lower())
        #print os.path.split(file_name_with_path)[0].lower().find(gf.lower())
        #print "len(os.path.split(file_name_with_path)[0].lower()) = %s" %len(os.path.split(file_name_with_path)[0].lower())
        #print "len(gf.lower())[0].lower()) = %s" %len(gf.lower())
        if os.path.split(file_name_with_path)[0].lower().find("\\"+gf.lower()+"\\") != -1:
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
    if file_without_path.lower().find("bluray") != -1:
        return "bluray"
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

def file_is_already_tagged(file_name_with_path):
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

def ignore_folder_present_in_path(file_with_path):
    my_path = os.path.split(file_with_path)[0]
    if my_path.lower().find(bad_file_trash.lower()) != -1:
        return True
    if my_path.lower().find(wrong_folder_trash.lower()) != -1:
        return True
    if my_path.lower().find(sample_trash.lower()) != -1:
        return True
    if my_path.lower().find(rejected_trash.lower()) != -1:
        return True
    if my_path.lower().find(unwanted_trash.lower()) != -1:
        return True
    if my_path.lower().find(duplicate_trash.lower()) != -1:
        return True
    if my_path.lower().find(icons_folder.lower()) != -1:
        return True
    return False

def is_rejected(file_with_path):
    """Return true if filde contains any of the rejected string"""
    spliteuh = os.path.split(file_with_path)
    file_name = spliteuh[1]
    
    for element in rejected:
        if file_name.lower().find(element) != -1:
            return True
    return False

def must_be_deleted(file_name_with_path, tag_key):
    """True if the file must be deleted, false if not"""
    unwanted_resolutions_list = get_tag_key_unwanted_resolutions_list(tag_key)
    quality_exception_list = get_tag_key_quality_exception_list(tag_key)
    file_quality = determine_quality(file_name_with_path)
    file_resolution = determine_resolution(file_name_with_path, file_quality)
    
    unwanted_resolution = False
    for ur in unwanted_resolutions_list:
        if ur == file_resolution:
            unwanted_resolution = True
    
    unwanted_quality = True
    if quality_exception_list is not False:
        for wq in quality_exception_list:
            if wq == file_quality:
                unwanted_quality = False

    if unwanted_resolution == True and unwanted_quality == True:
        return True
    return False
        
def get_tag_key(path_to_folder):
    """ return the tagkey if their is one, return false if their is none"""
    files_names = get_all_files_from(path_to_folder)
    for possible_tag_key in files_names:
        if possible_tag_key.lower().find("#delete#") == 0:
            return possible_tag_key
        return False

def get_tag_key_unwanted_resolutions_list(tag_key):
    """ Return a list of all unwanted resolution example : ["480p", "1080p"]"""
    if tag_key.lower().find("except") != -1:
        while tag_key.lower().find(".except") != -1:
            tag_key = os.path.splitext(tag_key)[0]
    unwanted_resolutions_list = []
    while True:
        unwanted_resolutions_list.append(os.path.splitext(tag_key)[1][1:])
        tag_key = os.path.splitext(tag_key)[0]
        if os.path.splitext(tag_key)[0] == "#delete#" and os.path.splitext(tag_key)[1] == '':
            break
    return unwanted_resolutions_list

def get_tag_key_quality_exception_list(tag_key):
    """ return a list of all quality exception list,
    return False is their is no exceptions"""
    quality_exception_list = []
    if tag_key.lower().find("except") != -1:
        while os.path.splitext(tag_key)[1] != ".except":
            quality_exception_list.append(os.path.splitext(tag_key)[1][1:])
            tag_key = os.path.splitext(tag_key)[0]
        return quality_exception_list
    else:
        return False
    
def is_tag_key(file_name):
    if file_name.lower().find("#delete#") != -1:
        return True
    return False

def debug_print(data):
    if DEBUG_MODE == True:
        print data

def remove_bad_file():
    print "step 1, sending bad file to %s" %os.path.split(bad_file_trash)[1]
    complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
    for file_name_with_path in complete_file_list:
        if not ignore_folder_present_in_path(file_name_with_path):
            if bad_file(file_name_with_path):
                debug_print("Sending %s to bad file trash" %os.path.split(file_name_with_path)[1])
                move_safely_to(bad_file_trash, file_name_with_path)

def locate_and_move_file_which_need_manual_sorting():
    print "step 2, moving file requiring manual sorting to %s " %os.path.split(wrong_folder_trash)[1]
    complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
    for file_name_with_path in complete_file_list:
        if not ignore_folder_present_in_path(file_name_with_path):
            if not is_in_good_folder(file_name_with_path):
                debug_print("Sending %s to manual sorting area" %os.path.split(file_name_with_path)[1])
                move_safely_to(wrong_folder_trash, file_name_with_path) 

def locate_and_move_foreign_file():
    print "step 3, moving rejected file (italian, spanish, russian, etc)"
    complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
    for file_name_with_path in complete_file_list:
        if not ignore_folder_present_in_path(file_name_with_path):
            if is_rejected(file_name_with_path):
                debug_print("Moving to rejected folder ! %s" %file_name_with_path)
                move_safely_to(rejected_trash, file_name_with_path)

def locate_and_move_unwanted_file():
    print "step 4, moving unwanted file to %s (according to folder tagKey)" %os.path.split(unwanted_trash)[1]
    complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
    for file_name_with_path in complete_file_list:
        if not is_tag_key(file_name_with_path):
            if not ignore_folder_present_in_path(file_name_with_path):
                tag_key = get_tag_key(os.path.split(file_name_with_path)[0])
                if tag_key != False:
                    if must_be_deleted(file_name_with_path, tag_key) is True:
                        debug_print("Moving to unwanted folder ! %s" %file_name_with_path)
                        move_safely_to(unwanted_trash, file_name_with_path)

def add_tag_to_files():
    print "step 5, tagging file (resolution+quality)"
    complete_file_list = get_all_files_from_folder_and_sub_folders(download_folder)
    for file_name_with_path in complete_file_list:
        if not ignore_folder_present_in_path(file_name_with_path):
            if not file_is_already_tagged(file_name_with_path):
                if not is_tag_key(file_name_with_path):
                    tag = determine_tag(file_name_with_path)
                    file_name_splitted = os.path.split(file_name_with_path)
                    debug_print("renaming %s to %s" %(file_name_splitted[1], tag+file_name_splitted[1]))
                    try:
                        os.rename(file_name_with_path, join(file_name_splitted[0], tag+file_name_splitted[1]))
                    except Exception:
                        debug_print("Plurality detected, moving to duplicate trash")
                        move_safely_to(duplicate_trash, file_name_with_path)


                        ##########################################
                        ##########################################
                        ##########################################
         #              #######                            #######
         #              ####### THIS IS THE ACTUAL PROGRAM #######
         #              #######                            #######
       #####            ##########################################
        ###             ##########################################
         #              ##########################################


print "Processing....."
remove_bad_file()
locate_and_move_file_which_need_manual_sorting()
locate_and_move_foreign_file()
#TODO Moving sample to sample location
locate_and_move_unwanted_file()
add_tag_to_files()
print "step 6, removing all empty folders"
remove_all_empty_folders(download_folder)
print "Processing done"
