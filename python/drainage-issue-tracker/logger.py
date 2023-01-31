import logging
import os
from logging.handlers import RotatingFileHandler
from util import joinPath, pathExists


def init():
    """start the logger and setup the handlers

    Returns:
        logger:
    """

    scriptpath = os.path.dirname(os.path.realpath(__file__))  # get the script path

    logFolder = joinPath(scriptpath, "logs")  # log folder path
    if not pathExists(logFolder):  # If log folder is not exist create
        os.mkdir(logFolder)

    logFile = joinPath(logFolder, "errorLogs.log")  # path to the error log file

    stringFormat = "%(asctime)s: -%(name)s: - %(levelname)s: - %(funcName)s: - Line:%(lineno)d:- %(message)s"  # format for the logger
    dateFormat = "%m/%d/%Y %I:%M:%S %p"  # date format for the error date

    logger = logging.getLogger()  # create a logger object

    logger.setLevel(logging.DEBUG)  # default logger level

    fileFormatter = logging.Formatter(
        fmt=stringFormat, datefmt=dateFormat
    )  # create a file formatter
    consoleFormatter = logging.Formatter(
        "%(name)s - %(levelname)s - %(message)s"
    )  # create a console log formatter

    consoleHandler = logging.StreamHandler()  # create a stream handler
    filterHandler = RotatingFileHandler(
        logFile, maxBytes=10000, backupCount=10
    )  # create a file rotating handler that will limit the file size and create up to 10 files

    filterHandler.setFormatter(fileFormatter)  # set the formatter
    consoleHandler.setFormatter(consoleFormatter)  # set the formatter

    filterHandler.setLevel(logging.ERROR)  # set loggin level
    consoleHandler.setLevel(logging.INFO)  # set loggin level

    logger.addHandler(filterHandler)  # add the file handler to the logger
    logger.addHandler(consoleHandler)  # add the console handler to the logger

    return logger  # return the logger
