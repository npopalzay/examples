from customError import AppError
import json
import os


def getValueIfExist(key, dic):
    """get value from a dic

    Args:
        key (str):
        dic (dict):

    Raises:
        AppError: if key not present

    Returns:
        any:
    """
    if key not in dic:
        raise AppError(f"{key} key not found")  # if key not present raise app error
    else:
        return dic[key]  # return the value


def writeToJson(data, filename):
    """save to a json file

    Args:
        data (dict):
        filename (str): json file path
    """
    with open(filename, "w") as out:
        json.dump(data, out)


def readJson(file):
    """read the json file

    Args:
        file (str): json file path

    Returns:
        dict:
    """
    return json.load(open(file))


def joinPath(firstPath, secondPath):
    """joins path

    Args:
        firstPath (str):
        secondPath (str):

    Returns:
        str: merge path
    """
    return os.path.join(firstPath, secondPath)


def pathExists(path):
    """check if path exists

    Args:
        path (str): folder path

    Returns:
        [bool]:
    """
    return os.path.exists(path)


def saveToHTML(message, fileName):
    """save the message to an HTML file

    Args:
        message (str):

    Returns:
        [type]: [description]
    """
    with open(fileName + ".html", "w") as file:
        file.write(message)
        file.close()


def addCss(message):

    # adding some css to the tables
    return (
        """<html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <style>
                .dataframe {
                    font-family: Arial, Helvetica, sans-serif;
                    border-collapse: collapse;
                }

                .dataframe td,
                .dataframe th {
                    border: 1px solid #ddd;
                    padding: 8px;
                }

                .dataframe tr:nth-child(even) {
                    background-color: #f2f2f2;
                }

                .dataframe th {
                    padding-top: 12px;
                    padding-bottom: 12px;
                    text-align: left;
                    color: gray;
                }
                </style>
            </head>
            <body>"""
        + f"{message}</body></html>"
    )
