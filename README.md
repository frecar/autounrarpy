autounrarpy
===========
Simple script to automatically unrar rar files in folder and subfolder.
It also deletes the oldest files in the folder and subfolders if the disk is full. It uses text files as log.

Usage:

    nice /usr/bin/python run.py /folder/ 10

Where 10 is the disk space (in GB) you want to have free. Warning: It will delete the oldest files if there is not enough space.
