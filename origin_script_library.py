#!/usr/bin/env python3

# Origin Script Library
# author: hypermodified
# This is a python library of code that is re-used across mutiple origin scripts
# Origin scripts use a yaml data structure called an origin file to provide metadata to organize, sort, tag and name music libraries


# Import dependencies
import os


# Common functions


# Get all the subdirectories of album_directory recursively and store them in a list
def set_directory(album_directory):
    try:
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included
    except:
        print("")
        print("--Error: There is a problem with the directory the script is trying to run in.")
        print("----Search the script for the phrase '#  Set your directories here'")
        print("----Check the the variable called 'album_directory' to make sure the directory assigned to that variable exists.")
    return directories
