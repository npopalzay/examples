import arcpy

class Service:
    address_locator = ""  # class variable for the address locator URL

    def GetFieldNameAndAlias(layer):
        """layar

        Args:
            layer (feature layer):

        Returns:
            dict: key value pair of fields with the name
        """
        return {field.name: field.aliasName for field in arcpy.ListFields(layer)}

    def SearchCursor(layer, fields, query, T):
        """search the layer or table and return an object

        Args:
            layer (layer or table):
            fields (list):
            query (str):
            T (any):

        Returns:
            any:
        """
        with arcpy.da.SearchCursor(layer, fields, query) as cursor:
            return [T(**dict(zip(cursor.fields, rowField))) for rowField in cursor]

    def QueryLayer(layer, outputLayer, query):
        """query layer and return a feature layer

        Args:
            layer (layer): input layer name
            outputLayer (layer): output layer name
            query (str):

        Returns:
            layer: output layer
        """
        return arcpy.MakeFeatureLayer_management(layer, outputLayer, query)

    def LineToPoint(layer, outputLayer):
        """converts a line feature layer to a point

        Args:
            layer (layer): input layer name
            outputLayer (layer): layer name

        Returns:
            layer: output layer
        """
        return arcpy.FeatureToPoint_management(layer, outputLayer, "CENTROID")

    def ReverseGeocode(layer, outputLayer):
        """reverse geocode a feature layer

        Args:
            layer (layer): =
            outputLayer (layer):

        Returns:
            layer: layer with address field
        """
        return arcpy.geocoding.ReverseGeocode(
            layer,
            Service.address_locator,
            outputLayer,
            "ADDRESS",
            "500 Feet",
        )
