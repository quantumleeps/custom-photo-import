# import all of the required modules
import pprint
import subprocess
import glob
import os
from shutil import copyfile
import tarfile
import datetime

# this function converts the terminal program exiftool's output
# into a dictionary file of exif data. Really all I'm using is 
# one tag, so maybe this program would be more efficient if I 
# did the other exiftool function that queries one tag...
def make_exif_dict(lines):
    exif_data = {}
    for x,y in enumerate(lines):
        b = y.decode("utf-8")
        c = b.find('  ')
        dict_left = b[0:c]
        d = b.find(':')
        e = len(b)
        f = e - d
        dict_right = b[(d+2):e]
        exif_data[dict_left] = dict_right
    return exif_data

# this takes a datetime and spits out the format that the filenames
# are to have
def date_formatter(dt):
    a = dt[0:4] + dt[5:7] + dt[8:10] + '_'
    a += dt[11:13] + dt[14:16] + dt[17:19] + dt[20:22]
    return a

# this function interfaces with the tarfile module to create a tarfile
# of the proper configuration
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# This is where you edit the locations of the respective directories
# involved with the program
sd_card_loc = '/Volumes/EOS_DIGITAL'
scratch_loc = '/Volumes/Storage'
backup_loc = '/Volumes/driveLeep v3'
tarfile_dir_loc = backup_loc + '/SD Card Backups'
tarfile_loc = tarfile_dir_loc + '/' + date_formatter(str(datetime.datetime.now())) + '.tar.gz'

# These are the subdirectory formats that the filenames are to follow
raw_dir_mod = '/Photography/Photos/Raw'
jpg_dir_mod = '/Photography/Photos/Jpg'
mov_dir_mod = '/Photography/Videos'

# The search strings at the end of the directory that the module Glob
# uses
jpg_glob_string = sd_card_loc + '/**/*.JPG'
cr2_glob_string = sd_card_loc + '/**/*.CR2'
rw2_glob_string = sd_card_loc + '/**/*.RW2'
mp4_glob_string = sd_card_loc + '/**/*.MP4'
# untested mov script
# mov_glob_string = sd_card_loc + '/**/*.MOV'

# The subprocess does a terminal command. The bytes format 
# is then converted into a dictionary using an above function.
# Directory structures are made that will represent the new file-
# name and the directory it goes into. Checks are made to see if
# the directory and/or filename exist before creating those. The
# below is repeated for any filetype that is to be imported
jpgs = glob.glob(jpg_glob_string, recursive=True)

for jpg in jpgs:
    lines = subprocess.check_output(['exiftool', jpg]).splitlines()
    exif_data = make_exif_dict(lines)
    photo_date = exif_data['Create Date']
    new_dir = scratch_loc + jpg_dir_mod + '/' + photo_date[0:4]
    new_filename = new_dir + '/' + date_formatter(photo_date) +  '.JPG'
    if os.path.isdir(new_dir):
        if os.path.exists(new_filename):
            print('Filename exists; keeping original')
        else:
            copyfile(jpg, new_filename)
    else:
        os.makedirs(new_dir)

cr2s = glob.glob(cr2_glob_string, recursive=True)

for cr2 in cr2s:
    lines = subprocess.check_output(['exiftool', cr2]).splitlines()
    exif_data = make_exif_dict(lines)
    photo_date = exif_data['Create Date']
    new_dir = scratch_loc + raw_dir_mod + '/' + photo_date[0:4]
    new_filename = new_dir + '/' + date_formatter(photo_date) +  '.CR2'
    if os.path.isdir(new_dir):
        if os.path.exists(new_filename):
            print('Filename exists; keeping original')
        else:
            copyfile(cr2, new_filename)
    else:
        os.makedirs(new_dir)

rw2s = glob.glob(rw2_glob_string, recursive=True)

for rw2 in rw2s:
    lines = subprocess.check_output(['exiftool', rw2]).splitlines()
    exif_data = make_exif_dict(lines)
    photo_date = exif_data['Create Date']
    new_dir = scratch_loc + raw_dir_mod + '/' + photo_date[0:4]
    new_filename = new_dir + '/' + date_formatter(photo_date) +  '.RW2'
    if os.path.isdir(new_dir):
        if os.path.exists(new_filename):
            print('Filename exists; keeping original')
        else:
            copyfile(rw2, new_filename)
    else:
        os.makedirs(new_dir)

mp4s = glob.glob(mp4_glob_string, recursive=True)

for mp4 in mp4s:
    lines = subprocess.check_output(['exiftool', mp4]).splitlines()
    exif_data = make_exif_dict(lines)
    photo_date = exif_data['Create Date']
    new_dir = scratch_loc + mov_dir_mod + '/' + photo_date[0:4]
    new_filename = new_dir + '/' + date_formatter(photo_date) +  '.MP4'
    if os.path.isdir(new_dir):
        if os.path.exists(new_filename):
            print('Filename exists; keeping original')
        else:
            copyfile(mp4, new_filename)
    else:
        os.makedirs(new_dir)
# Need to add in .mov here. Need to add the appropriate initializing
# lists, etc. above and glob search queries.

# untested mov script
# # movs = glob.glob(mov_glob_string, recursive=True)

# for mov in movs:
#     lines = subprocess.check_output(['exiftool', mov]).splitlines()
#     exif_data = make_exif_dict(lines)
#     photo_date = exif_data['Create Date']
#     new_dir = scratch_loc + mov_dir_mod + '/' + photo_date[0:4]
#     new_filename = new_dir + '/' + date_formatter(photo_date) +  '.MP4'
#     if os.path.isdir(new_dir):
#         if os.path.exists(new_filename):
#             print('Filename exists; keeping original')
#         else:
#             copyfile(mov, new_filename)
#     else:
#         os.makedirs(new_dir)