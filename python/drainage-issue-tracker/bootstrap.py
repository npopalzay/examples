from customError import AppError
import os
import datetime
from util import joinPath, getValueIfExist, writeToJson, readJson, pathExists


class Boostrap:
    def __init__(self):
        self.dateformat = "%m/%d/%Y %I:%M:%S %p"  # date formart

        dateTrackerFolderName = "tracker"  # name of the tracking folder

        scriptpath = os.path.dirname(os.path.realpath(__file__))  # get the script path

        # get the app config file
        configFile = joinPath(scriptpath, "appConfig.json")

        if not os.path.isfile(configFile):  # Check if config file exist
            raise AppError("Config file not found")

        self.configJson = readJson(configFile)  # read the config json file

        connectionString = getValueIfExist(
            "connectionString", self.configJson
        )  # get the connection string dictionary

        gdbName = getValueIfExist("gdbName", connectionString)  # get the GDB name
        layers = getValueIfExist("layers", self.configJson)  # get the layers dic
        tables = getValueIfExist("tables", self.configJson)  # get the tables dic

        connectionFile = joinPath(scriptpath, gdbName)  # GDB workspace path

        self.trackTime = getValueIfExist(
            "trackTime", self.configJson
        )  # check the track time mode
        self.sendEmail = getValueIfExist(
            "sendEmail", self.configJson
        )  # check the send email mode

        self.segmentLayerName = joinPath(
            connectionFile, getValueIfExist("segmentLayerName", layers)
        )  # segment layer path

        self.pointLayerName = joinPath(
            connectionFile, getValueIfExist("pointLayerName", layers)
        )  # point layer path

        self.segmentTableName = joinPath(
            connectionFile, getValueIfExist("segmentInspectionTableName", tables)
        )  # segment inspection table path

        self.segmentDetailTable = joinPath(
            connectionFile, getValueIfExist("segmentDetailTable", tables)
        )  # segment detail table path

        self.pointTableName = joinPath(
            connectionFile, getValueIfExist("pointInspectionTableName", tables)
        )  # point inspection table path

        self.addressLocator = getValueIfExist(
            "addressLocator", self.configJson
        )  # get the address locator URL

        dateTrackerFolder = joinPath(
            scriptpath, dateTrackerFolderName
        )  # date tracking folder path

        # If tracking folder is not exist create
        if not pathExists(dateTrackerFolder):
            os.mkdir(dateTrackerFolder)

        dateTrackerFileName = getValueIfExist(
            "dateTrackerFileName", self.configJson
        )  # get the tracking file name

        self.dateTrackingFile = joinPath(
            dateTrackerFolder, dateTrackerFileName
        )  # date tracker file path

        self.nowUTCDateTimeString = self.getUTCTime()  # get the current UTC time

        # Check if the date tracker file exist if not create one and save the current UTC datetime
        if not pathExists(self.dateTrackingFile):
            self.saveCurrentUTCTime()

        # read the date tracking file
        trackerJson = readJson(self.dateTrackingFile)

        # get the last check datetime from the json file
        lastCheckDateFromFile = datetime.datetime.strptime(
            getValueIfExist("LastCheckDate", trackerJson), self.dateformat
        )
        # convert the date object to time string
        self.lastCheckedDateString = datetime.datetime.strftime(
            lastCheckDateFromFile, self.dateformat
        )

    def getUTCTime(self):
        nowUTCTime = datetime.datetime.utcnow()  # Get the current UTC time
        return datetime.datetime.strftime(
            nowUTCTime, self.dateformat
        )  # Convert UTC datetime object to string for saving

    def saveCurrentUTCTime(self):
        lastCheckedDateDict = {"LastCheckDate": self.nowUTCDateTimeString}
        # write data to a json
        writeToJson(lastCheckedDateDict, self.dateTrackingFile)
