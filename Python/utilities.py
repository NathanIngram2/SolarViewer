"""
File: utilities.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Additional utilities for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""


class Log:
    """
    Logging utility for the Solar Eclipse Viewer project.
    """
    verbose = "HIGH"

    def __init__(self, verbosity):
        """
        Initialize the logging utility with a specified verbosity level.

        :param verbosity: Verbosity level (LOW, MED, HIGH).
        """
        Log.verbose = verbosity

    # Low priority info log
    @staticmethod
    def info(msg):
        if Log.verbose == "HIGH":
            print("INFO: " + msg)
        return

    # High priority info log
    @staticmethod
    def warn(msg):
        if Log.verbose == "HIGH" or Log.verbose == "MED":
            print("WARN: " + msg)
        return

    # Error log. Always printed.
    @staticmethod
    def error(msg):
        print("ERROR: " + msg)
