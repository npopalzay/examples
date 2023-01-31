class SegmentBase:
    """base class for segments"""

    def __init__(self, **kwargs):
        if "SEG_ID" in kwargs:
            self.SEG_ID = kwargs["SEG_ID"]


class SegmentAddress(SegmentBase):
    """class for segment addresses

    Args:
        SegmentBase (SegmentBase):
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "REV_Match_addr" in kwargs:
            self.MatchAddress = kwargs["REV_Match_addr"]


class DrainageSegmentDetailTable(SegmentBase):
    """class for the segments detail table

    Args:
        SegmentBase (SegmentBase):
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "ASB_LEN" in kwargs:
            self.AS_BUILT_LENGTH = kwargs["ASB_LEN"]


class DrainageInspectionBase:
    """base class for the inspection tables"""

    def __init__(self, **kwargs):
        if "TypeofInspection" in kwargs:
            self.TypeofInspection = kwargs["TypeofInspection"]
        if "MajorIssue" in kwargs:
            self.MajorIssue = kwargs["MajorIssue"]
        if "InspectorComment" in kwargs:
            self.InspectorComment = kwargs["InspectorComment"]
        if "InspectedBy" in kwargs:
            self.InspectedBy = kwargs["InspectedBy"]
        if "InspectionDate" in kwargs:
            self.InspectionDate = kwargs["InspectionDate"]
        if "Last_Edited_By" in kwargs:
            self.Last_Edited_By = kwargs["Last_Edited_By"]
        if "Last_Edited_Date" in kwargs:
            self.Last_Edited_Date = kwargs["Last_Edited_Date"]
        if "GlobalID" in kwargs:
            self.GlobalID = kwargs["GlobalID"]


class DrainageSegmentInspectionTable(SegmentBase, DrainageInspectionBase):
    """class for the segment inspections

    Args:
        SegmentBase (SegmentBase):
        DrainageInspectionBase (DrainageInspectionBase):
    """

    def __init__(self, **kwargs):
        SegmentBase.__init__(self, **kwargs)
        DrainageInspectionBase.__init__(self, **kwargs)

    def __str__(self) -> str:
        return f"{self.SEG_ID},{self.TypeofInspection}, {self.MajorIssue}, {self.InspectorComment}, {self.InspectedBy}, {self.InspectionDate}"


class PointBase:
    """base class for the points"""

    def __init__(self, **kwargs):
        if "STRUC_ID" in kwargs:
            self.STRUC_ID = kwargs["STRUC_ID"]


class PointAddress(PointBase):
    """class for the point addresses

    Args:
        PointBase (PointBase):
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "REV_Match_addr" in kwargs:
            self.MatchAddress = kwargs["REV_Match_addr"]


class DrainagePointInspectionTable(PointBase, DrainageInspectionBase):
    """class for the inspected points

    Args:
        PointBase (PointBase):
        DrainageInspectionBase (DrainageInspectionBase):
    """

    def __init__(self, **kwargs):
        PointBase.__init__(self, **kwargs)
        DrainageInspectionBase.__init__(self, **kwargs)

    def __str__(self) -> str:
        return f"{self.STRUC_ID},{self.TypeofInspection}, {self.MajorIssue}, {self.InspectorComment}, {self.InspectedBy}, {self.InspectionDate}"
