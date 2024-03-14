"""
File: solar_viewer_utilites.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-11-25
Description: Utilities for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.

Copyright (C) 2023  Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

VERBOSE = False

def info(msg):
    if VERBOSE:
        print("INFO: " + msg)

def warn(msg):
    print("WARN: " + msg)

def error(msg):
    print("ERROR: " + msg)


