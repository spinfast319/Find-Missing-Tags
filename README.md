# Find-Missing-Tags
### This python script loops through a directory and looks for albums that are missing track number, title, artist, or album tags, and then moves the album containing those tracks to a folder for retagging. 

After finding the tracks and moving the albums, it provides messaging and logs what it does so you can look up what it moved. It doesn't specify which tags are missing, you will need to use tagging software to investigate the albums moved. If you have a large music collection you can use this to quickly find albums that need the core tags to be fixed for music players to read them correctly.

It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters. It has been tested and works in both Ubuntu Linux and Windows 10. You will need to install the mutagen library with pip for it to work.

## Install and set up
1) Clone this script where you want to run it.

2) Install [mutagen](https://pypi.org/project/mutagen/) with pip. (_note: on some systems it might be pip3_) 

to install it:

```
pip install mutagen
```

3) Edit the script where it says _Set your directories here_ to set up or specify three directories you will be using. Write them as absolute paths for:

    A. The directory where the albums you want to examine for missing tags are stored  
    B. The directory to store the log files the script creates  
    C. The directory where you want the albums with bad tags to be moved to.

4) Edit the script where it says _Set whether you are using nested folders_ to specify whether you are using nested folders or have all albums in one directory 

    A. If you have all your ablums in one music directory, ie. Music/Album then set this value to 1 (the default)  
    B. If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2

5) Use your terminal to navigate to the directory the script is in and run the script from the command line.  When it finishes it will output how many albums were moved for missing tags.

```
Find-Missing-Tags.py
```

_note: on linux and mac you will likely need to type "python3 Find-Missing-Tags.py"_  
_note 2: you can run the script from anywhere if you provide the full path to it_

The script will also create logs listing all the albums it moved and include the original path and the new path.  

