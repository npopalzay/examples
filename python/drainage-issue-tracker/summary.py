from service import Service
import pandas as pd
from drainageDataModel import (
    SegmentAddress,
    PointAddress,
    DrainagePointInspectionTable,
    DrainageSegmentInspectionTable,
    DrainageSegmentDetailTable,
)


class Summary:
    """base class for the reports"""

    def __init__(self, **kwargs):
        if "table" in kwargs:
            self.table = kwargs["table"]
            self.tableFieldNameAndAlias = Service.GetFieldNameAndAlias(
                kwargs["table"]
            )  # get the field names
        if "layer" in kwargs:
            self.layer = kwargs["layer"]
            self.layerFieldNameAndAlias = Service.GetFieldNameAndAlias(
                kwargs["layer"]
            )  # get the field names
        if "lastCheckedDateString" in kwargs:
            self.lastCheckedDateString = kwargs["lastCheckedDateString"]

            self.query = f"""InspectionDate > timestamp '{self.lastCheckedDateString}' OR Last_Edited_Date > timestamp'{self.lastCheckedDateString}'"""  # build a query string to check for the new records

        # placeholders object properties
        self.queryLayer = ""
        self.addresses = ""
        self.addressesDataframe = None
        self.dataframeWithAddresses = None
        self.dataframe = None

    def QueryTable(self):
        """query table for new records"""
        pass

    def GetFeatures(self):
        """get the features from the layer file"""
        pass

    def GetAddresses(self):
        """reverse geocode the addresses using geometry"""
        pass

    def GetDataframe(self):
        """generate the pandas dataframe"""
        pass

    def _getDataframe(elements):
        """local auxiliary function to create a data frame using object properties

        Args:
            elements (list):

        Returns:
            dataframe:
        """
        return pd.DataFrame.from_records(element.__dict__ for element in elements)

    def GetAddressesDataframe(self):
        """generate the addresses dataframe

        Returns:
            self:
        """
        self.addressesDataframe = Summary._getDataframe(self.addresses)
        return self


class PointSummary(Summary):
    """point summary class

    Args:
        Summary (base):
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # placeholders
        self.points = []
        self.dataframe = None

    def QueryTable(self):
        self.points.clear()  # clear the points list
        self.points = Service.SearchCursor(
            self.table,
            list(self.tableFieldNameAndAlias.keys()),
            self.query,
            DrainagePointInspectionTable,
        )  # query the table using the last checked date and time
        return self

    def GetFeatures(self):
        # create the query string for all the points
        query = f"STRUC_ID IN {tuple(i.STRUC_ID for i in self.points)}"
        self.queryLayer = Service.QueryLayer(
            self.layer, "memory\pointQueryLayer", query
        )  # create an in memory layer
        return self

    def GetAddresses(self):
        if self.queryLayer:  # check if there are features
            matchAddressLayer = Service.ReverseGeocode(
                self.queryLayer, r"memory\pointAddresses"
            )  # revese geocode the point layer
            if matchAddressLayer:
                self.addresses = Service.SearchCursor(
                    matchAddressLayer,
                    ["STRUC_ID", "REV_Match_addr"],
                    None,
                    PointAddress,
                )  # query the layer and get the addresses
        return self

    def GetDataframe(self):
        self.dataframe = Summary._getDataframe(
            self.points
        )  # generate a dataframe for the points
        return self


class SegmentSummary(Summary):
    """segment summary class

    Args:
        Summary (base):
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if "segmentDetailTable" in kwargs:
            self.segmentDetailTable = kwargs["segmentDetailTable"]
            self.detailTableNameAndAlias = Service.GetFieldNameAndAlias(
                self.segmentDetailTable
            )  # get the field names
        # placeholders
        self.segmentsDetail = []
        self.segments = []
        self.segmentWithDetailsDataframe = None
        self.segmentDetailsDataframe = None

    def QueryTable(self):
        self.segments.clear()  # clear the segments list
        self.segments = Service.SearchCursor(
            self.table,
            list(self.tableFieldNameAndAlias.keys()),
            self.query,
            DrainageSegmentInspectionTable,
        )  # search for table for new records using the last checked date
        return self

    def LoadDetailTable(self):
        query = f"SEG_ID IN {tuple(i.SEG_ID for i in self.segments)}"
        self.segmentsDetail = Service.SearchCursor(
            self.segmentDetailTable,
            list(self.detailTableNameAndAlias.keys()),
            query,
            DrainageSegmentDetailTable,
        )  # search the detail table and get the records
        return self

    def GetFeatures(self):
        # generate a query string for using the segment ids
        query = f"SEG_ID IN {tuple(i.SEG_ID for i in self.segments)}"
        queryLineLayer = Service.QueryLayer(
            self.layer, r"memory\segmentLineQueryLayer", query
        )  # query the segment layer
        self.queryLayer = Service.LineToPoint(
            queryLineLayer, r"memory\segmentPointQueryLayer"
        )  # convert segments to point for reverse geocoding
        return self

    def GetAddresses(self):
        if self.queryLayer:  # check if the query layer is exists
            matchAddressLayer = Service.ReverseGeocode(
                self.queryLayer, r"memory\segmentAddresses"
            )  # reverse goecode
            if matchAddressLayer:
                self.addresses = Service.SearchCursor(
                    matchAddressLayer,
                    ["SEG_ID", "REV_Match_addr"],
                    None,
                    SegmentAddress,
                )  # get the addresses
        return self

    def GetDataframe(self):
        self.dataframe = Summary._getDataframe(
            self.segments
        )  # generate segments dataframe
        return self

    def GetSegmentDetailDataframe(self):
        self.segmentDetailsDataframe = Summary._getDataframe(
            self.segmentsDetail
        )  # generate segment details dataframe
        return self
