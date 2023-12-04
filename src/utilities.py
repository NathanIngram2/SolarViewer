"""
File: utilities.py
Author: Will Conway, Devynn Garrow, Ben Graham, Jessica Guetre, Nathan Ingram
Date: 2023-10-25
Description: Additional utilities for the Solar Eclipse Viewer project for ENPH454 @ Queen's University, Kingston ON.
"""

import datetime
import os

class Log:
    """
    Logging utility for the Solar Eclipse Viewer project.
    """
    VERBOSE = "HIGH"
    strDateTime = None
    logDirPath = None
    logFilePath = None
    logFile = None

    def __init__(self, args, callingFile):
        """
        Initialize the logging utility with a specified verbosity level.

        :param verbosity: Verbosity level (LOW, MED, HIGH).
        """
        Log.VERBOSE = args.verbose

        Log.strDateTime = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        Log.logDirPath = os.path.join("Log", Log.strDateTime)
        try:
            os.mkdir(Log.logDirPath)
        except FileNotFoundError:
            os.mkdir("Log")
            os.mkdir(Log.logDirPath)

        Log.logFilePath = os.path.join(Log.logDirPath, "LOG" + Log.strDateTime + ".txt")
        Log.logFile = open(Log.logFilePath, "x")
        Log.logFile.write("Run from " + callingFile + "\n" + str(args).replace("Namespace(", "Command Line Args:")
                          .replace(")", "\n\n------------------------------------------------------\n\n"))
        Log.logFile.close()

    # Low priority info log
    @staticmethod
    def info(msg):
        Log.logFile = open(Log.logFilePath, "a")
        Log.logFile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " INFO: " + msg + "\n")
        Log.logFile.close()
        if Log.VERBOSE == "HIGH":
            print("INFO: " + msg)
        return

    # High priority info log
    @staticmethod
    def warn(msg):
        Log.logFile = open(Log.logFilePath, "a")
        Log.logFile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " WARN: " + msg + "\n")
        Log.logFile.close()
        if Log.VERBOSE == "HIGH" or Log.VERBOSE == "MED":
            print("WARN: " + msg)
        return

    # Error log. Always printed.
    @staticmethod
    def error(msg):
        Log.logFile = open(Log.logFilePath, "a")
        Log.logFile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " ERROR: " + msg + "\n")
        Log.logFile.close()
        print("ERROR: " + msg)
