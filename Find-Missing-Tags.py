#!/usr/bin/env python3

# Find Missing Tags
# author: hypermodified
# This python script loops through a directory and looks for albums that are missing track number, title, artist, or album tags
# It moves the album containing those tracks to a folder for retagging.
# This has only been tested to work with flac files.
# It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters.
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Before running this script install the dependencies
# pip install mutagen

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import shutil  # Imports functionality that lets you copy files and directory
import datetime  # Imports functionality that lets you make timestamps
import mutagen  # Imports functionality to get metadata from music files

#  Set your directories here
album_directory = "M:\PROCESS"  # Which directory do you want to start with?
log_directory = "M:\PROCESS-LOGS\Logs"  # Which directory do you want the log in?
sort_directory = "M:\Python Test Environment\Sort - Missing Tags"  # Directory to move albums missing tags to

# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1

# Establishes the counters for completed albums and missing origin files
count = 0
total_count = 0
error_message = 0
tags_missing = 0

# identifies album directory level
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
album_location = segments + album_depth

# creates the list of albums that need to be moved post sorting
move_set = set()

# A function to log events
def log_outcomes(directory, log_name, message):
    global log_directory

    script_name = "Find Missing Tags"
    today = datetime.datetime.now()
    log_name = f"{log_name}.txt"
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = os.path.join(log_directory, log_name)
    with open(log_path, "a", encoding="utf-8") as log_name:
        log_name.write(f"--{today:%b, %d %Y} at {today:%H:%M:%S} from the {script_name}.\n")
        log_name.write(f"The album folder {album_name} {message}.\n")
        log_name.write(f"Album location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# A function that determines if there is an error
def error_exists(error_type):
    global error_message

    if error_type >= 1:
        error_message += 1  # variable will increment if statement is true
        return "Warning"
    else:
        return "Info"


# A function that writes a summary of what the script did at the end of the process
def summary_text():
    global count
    global total_count
    global error_message
    global tags_missing

    print("")
    print(f"This script moved {count} albums for having bad tags out of {total_count} albums examined.")
    print("This script looks for potential missing files or errors. The following messages outline whether any were found.")

    error_status = error_exists(tags_missing)
    print(f"--{error_status}: There were {tags_missing} albums missing either track number, title, artist or album tags. They were moved to the Missing Tags folder.")

    if error_message >= 1:
        print("Check the logs to see which folders were moved.")
    else:
        print("There were no errors.")


# A function to move albums to the correct folder
def move_albums(move_set):
    global count

    # Loop through the list of albums to move
    for i in move_set:

        # Break each entry into a source and target
        start_path = i[0]
        target = i[1]

        # Move them to the folders they belong in
        print("")
        print("Moving.")
        print(f"--Source: {start_path}")
        print(f"--Destination: {target}")
        shutil.move(start_path, target)
        print("Move completed.")
        count += 1  # variable will increment every loop iteration


# A function to check whether the directory is a an album or a sub-directory
def level_check(directory):
    global total_count
    global album_location

    print("")
    print(directory)
    print("Folder Depth:")
    print(f"--The albums are stored {album_location} folders deep.")

    path_segments = directory.split(os.sep)
    directory_location = len(path_segments)

    print(f"--This folder is {directory_location} folders deep.")

    # Checks to see if a folder is an album or subdirectory by looking at how many segments are in a path
    if album_location == directory_location:
        print("--This is an album.")
        total_count += 1  # variable will increment every loop iteration
        return True
    elif album_location < directory_location:
        print("--This is a sub-directory")
        return False
    elif album_location > directory_location and album_depth == 2:
        print("--This is an artist folder.")
        return False


# A function to check whether a directory has flac and should be checked further
def flac_check(directory):

    # Loop through the directory and see if any file is a flac
    for fname in os.listdir(directory):
        if fname.endswith(".flac"):
            print("--There are flac in this directory.")
            return True

    print("--There are no flac in this directory.")
    return False


# A function to check the tags of each file and sort it if critical tags are missing
def tag_check(directory, is_album):
    global sort_directory
    global album_location
    global album_directory
    global move_set
    global tags_missing
    global album_depth

    # Get the album name
    segments = directory.split(os.sep)
    album_location_index = album_location - 1
    album_name = str(segments[album_location_index])

    # If the album depth is 2, get the artist name
    if album_depth == 2:
        artist_location_index = album_location - 2
        artist_name = str(segments[artist_location_index])

    # Handle directories vs sub-directories by defining start path taking into account is_album depth
    if is_album == True:
        start_path = directory
    elif album_depth == 1:
        # build the path by joining the album directory path with the album name
        start_path = os.path.join(album_directory, album_name)
    elif album_depth == 2:
        # build the path by joining the album directory path with the artist and album name
        start_path = os.path.join(album_directory, artist_name, album_name)

    # loop through directory and look for missing tags
    for fname in os.listdir(directory):
        if fname.endswith(".flac"):
            meta_data = mutagen.File(fname)
            if "tracknumber" not in meta_data or "artist" not in meta_data or "title" not in meta_data or "album" not in meta_data:
                print("--Failure: Metadata Missing")
                print("--This should be moved to the Missing Tags folder.")
                if album_depth == 1:
                    target = os.path.join(sort_directory, album_name)
                elif album_depth == 2:
                    target = os.path.join(sort_directory, artist_name, album_name)
                print(f"--The starting path is: {start_path}")
                print(f"--The target is: {target}")
                # make the pair a tupple
                move_pair = (start_path, target)
                # adds the tupple to the list
                move_set.add(move_pair)
                # log the album is  missing tags
                print("--Logged missing tags.")
                log_name = "tags_missing"
                log_message = f"has tracks that are missing either track number, title, artist or album tags.\nIt has been moved to: {target}"
                log_outcomes(directory, log_name, log_message)
                tags_missing += 1  # variable will increment every loop iteration
                return False

    return True


# The main function that controls the flow of the script
def main():
    global move_set
    global album_location

    try:
        # intro text
        print("")
        print("You Have My Sword, and My Bow...")
        print("")
        print("Part 1: Sorting")

        # Get all the subdirectories of album_directory recursively and store them in a list:
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included

        #  Run a loop that goes into each directory identified in the list and runs the function that sorts the folders
        for i in directories:
            os.chdir(i)  # Change working Directory
            # establish directory level
            is_album = level_check(i)
            # check for flac
            is_flac = flac_check(i)
            # check for meta data and sort
            if is_flac == True:
                tag_check(i, is_album)

        # Change directory so the album directory can be moved and move them
        os.chdir(log_directory)

        # Move the albums to the folders the need to be sorted into
        print("")
        print("Part 2: Moving")
        move_albums(move_set)

    finally:
        # Summary text
        print("")
        print("...and My Axe")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()
