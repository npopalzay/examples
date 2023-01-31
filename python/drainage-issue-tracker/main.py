from customError import AppError, EmailError
from emailClient import EmailClient
from service import Service
from summary import PointSummary, SegmentSummary
from bootstrap import Boostrap
import sys
import logger as log
from util import saveToHTML, addCss


def main():
    """main function of the script"""
    try:
        logger = log.init()  # init the logger
        boot = Boostrap()  # init the bootstrap module
        # init the email sender module
        email = EmailClient(configJson=boot.configJson)
        emailContent = []  # placeholder for the email body

        Service.address_locator = boot.addressLocator  # get the address locator

        logger.info(
            boot.lastCheckedDateString
        )  # log on console the start time of the script on

        pointSummary = PointSummary(
            table=boot.pointTableName,
            layer=boot.pointLayerName,
            lastCheckedDateString=boot.lastCheckedDateString,
        )  # create a point summary class

        pointSummary.QueryTable()  # query for new inspection records since last check
        if len(pointSummary.points) > 0:  # check if there is a new record
            # get the features and then reverse geocode
            pointSummary.GetFeatures().GetAddresses()
            pointSummary.GetDataframe().GetAddressesDataframe()  # get the panda dataframe

            pointWitAddress = pointSummary.dataframe.merge(
                pointSummary.addressesDataframe
            )  # merge the addresses to the main dataframe

            sortedpointWithAddress = pointWitAddress.sort_values(
                by=["InspectionDate", "InspectedBy"]
            )  # sort the values by inspection date and inspector name

            pointGroupByName = (
                sortedpointWithAddress[["InspectedBy", "STRUC_ID"]]
                .groupby("InspectedBy")["STRUC_ID"]
                .count()
                .reset_index(name="Count")
            )  # count the number of inspection done by each inspector

            sortedpointWithAddress.drop(
                ["GlobalID"], axis=1, inplace=True
            )  # remove the Global id colum

            pointHtml = sortedpointWithAddress.to_html(index=False).replace(
                "NaN", ""
            )  # create html
            pointsCountHtml = pointGroupByName.to_html(
                index=False
            )  # create points county html and

            emailContent.append(
                f"<h3>Points</h3>{pointHtml}"
            )  # add to the email body content
            emailContent.append(
                f"<h4>Summary</h4>{pointsCountHtml}"
            )  # add to the email body content

        segmentSummary = SegmentSummary(
            table=boot.segmentTableName,
            layer=boot.segmentLayerName,
            lastCheckedDateString=boot.lastCheckedDateString,
            segmentDetailTable=boot.segmentDetailTable,
        )  # create a segment summary class

        segmentSummary.QueryTable()  # query for new inspection records since last check
        if len(segmentSummary.segments) > 0:
            segmentSummary.LoadDetailTable()  # check if there is a new record

            # get the features and then reverse geocode
            segmentSummary.GetFeatures().GetAddresses()

            segmentSummary.GetDataframe().GetSegmentDetailDataframe().GetAddressesDataframe()  # get dataframes for each tables

            segmentsWithDetail = segmentSummary.dataframe.merge(
                segmentSummary.segmentDetailsDataframe
            )  # merge the segment dataframe with the main segment dataframe

            segmentWithDetailAndAddress = segmentsWithDetail.merge(
                segmentSummary.addressesDataframe
            )  # merge the addressed dataframe with the segment and detail dataframe

            sortedSegmentsWithDetailAndAddress = (
                segmentWithDetailAndAddress.sort_values(
                    by=["InspectionDate", "InspectedBy"]
                )
            )  # sort the dataframe by inspection date and inspector name

            segmentsGroupByName = (
                sortedSegmentsWithDetailAndAddress[["InspectedBy", "AS_BUILT_LENGTH"]]
                .groupby("InspectedBy")
                .sum()
            ).rename(
                columns={"AS_BUILT_LENGTH": "As-built length (ft)"}
            )  # calculate the as-built length each

            sortedSegmentsWithDetailAndAddress.drop(
                ["GlobalID"], axis=1, inplace=True
            )  # remove the Global id colum

            segmentHtml = sortedSegmentsWithDetailAndAddress.to_html(
                index=False
            ).replace(
                "NaN", ""
            )  # remove NaN from the records  # create html
            segmentSumHtml = segmentsGroupByName.to_html()  # create html

            emailContent.append(
                f"<h3>Segments</h3>{segmentHtml}"
            )  # add to the email body content

            emailContent.append(
                f"<h4>Summary</h4>{segmentSumHtml}"
            )  # add to the email body content

        if len(emailContent) > 0:  # check if there is any content to send
            # convert the list to a string
            emailBodyString = "".join(emailContent)

            if boot.sendEmail:
                email.sendInspectionEmail(
                    addCss(emailBodyString)
                )  # add some css and send an email
            else:
                htmlFileName = "Index"
                saveToHTML(
                    addCss(emailBodyString), htmlFileName
                )  # add same some css and save as an HTML file in the root folder
            if boot.trackTime:
                boot.saveCurrentUTCTime()  # save the new date in the tracker json

    except EmailError as e:
        logger.exception(
            e.message
        )  # if any problem with the smtp, just log the error in the log file
    except AppError as e:
        logger.exception(e.message)  # save the error in the log file
        if boot.sendEmail:
            email.SendErrorMessage(e)  # email the error to the admin
    except Exception as e:
        # save the error in the log file
        logger.exception("Something went wrong!")
        if boot.sendEmail:
            email.SendErrorMessage(e)  # email the error to the admin


if __name__ == "__main__":
    sys.exit(int(main() or 0))
