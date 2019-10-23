import importlib
import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras import models
sys.stderr = stderr
from functools import lru_cache
from common_utils import S3Util
import pandas as pd
from sklearn.externals import joblib
from common_utils.MLLogger import MLLogging
from filelock import FileLock
from threading import Lock

s3Config= S3Util.S3Configuration()
logger=MLLogging.getLog()

def parseS3filePath(s3FilePath):
    """
    Parse the S3 file Path and extract S3 Bucket name and S3 file location.
    s3FilePath Convention: /s3-<bucket-name>/<path/to/file/in/local/and/s3>
    If it is not parseable it will return the as is s3FilePath as the localFilePath(assuming the string is the S3 object key) and None as the bucketName

    :param s3FilePath: the Complete File Path Location including S3 bucket and the file with directory location

    :return: Splits the string to get bucket name and s3 file location according to the convention
    """
    bucketName=None
    localFilePath=None
    if s3FilePath.startswith("/s3-"):
        localFilePath= s3FilePath[s3FilePath[1:].index("/") + 2:]
        bucketName= s3FilePath[:s3FilePath[1:].index("/") + 1][1:]
    elif s3FilePath.startswith("s3-"):
        localFilePath = s3FilePath[s3FilePath.index("/") + 1:]
        bucketName = s3FilePath[:s3FilePath.index("/")]
    else:
        localFilePath=s3FilePath
    return bucketName,localFilePath

def makeDirectories(localFileLocation):
    """
    Makes directories in the location of file prior to file creation
    [FORMAT: 'folder1/folder2/filename']

    :param localFileLocation: The location of file where the directories are to be created prior to file creation

    :return: None
    """
    try:
        localFilePath = localFileLocation[:localFileLocation.rindex("/")]
        if not os.path.exists(localFilePath):
            os.makedirs(localFilePath)
    except FileExistsError:
        logger.debug("Folders already Exists")
        pass

def fetchFileFromS3viaLocalApi(s3FullPath,s3Direct=False):
    """
    Takes S3fullPath and downloads the file and return localFileLocation

    :param s3FullPath: S3 file location to download

    :return: localFileLocation of the downloaded file
    """
    try:
        s3util = S3Util.S3LocalUtility()
        bucketName, s3filePath = parseS3filePath(s3FullPath)
        localFileLocation = s3util.s3Config.s3_local_folder_path + s3filePath
        logger.info(localFileLocation)
        if os.path.isfile(localFileLocation) and s3Direct is False:
            return localFileLocation
        if bucketName is None:
            raise FileNotFoundError("Bucket not well defined according to format and no file was found in local file system"+str(localFileLocation))
        makeDirectories(localFileLocation)
        with FileLock(str(localFileLocation)+".lock"):
            with Lock():
                if not os.path.isfile(localFileLocation) or s3Direct is True:
                    logger.info("Downloading file from S3: Bucket: " + str(bucketName) + " S3 file path: " + str(s3filePath) + " via Local API")
                    s3util.downloadFileFromS3(s3filePath, localFileLocation, bucketName)
        return localFileLocation
    except Exception as e:
        msg = "Exception While downloading file from S3 Utility: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

@lru_cache(maxsize=20)
def load_pipeline_cache(s3FullFilePath):
    """

    Load the file into the memory using a LRU Caching of maxsize by deriving location and appending local S3 storage path with relative s3 file path

    :param s3FullFilePath: S3 file location for the model

    :return: Pickle Object
    """
    try:
        bucketName, s3FilePath = parseS3filePath(s3FullFilePath)
        localFileLocation = s3Config.s3_local_folder_path + s3FilePath
        return joblib.load(localFileLocation)
    except Exception as e:
        msg = "Exception While loading the model from a file: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def load_h5_file(s3FullFilePath):
    """
    Load the Keras specific h5 model file from the local file system

    :param s3FullFilePath: S3 file location for the model

    :return: keras model file
    """
    try:
        bucketName, s3FilePath = parseS3filePath(s3FullFilePath)
        localFileLocation = s3Config.s3_local_folder_path + s3FilePath
        return models.load_model(localFileLocation)
    except Exception as e:
        msg = "Exception While loading the keras model configs from a h5 file: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def readCsvFromS3(s3FullPath,s3Direct=True,**kwargs):
    """
    Read csv file from S3 given the S3file path

    :param s3FullPath: csv S3 file path

    :param s3Direct: if True always downloads from S3, else searches in local and returns if found

    :param kwargs: arguments to read_csv

    :return: csv file
    """
    try:
        localFileLocation=fetchFileFromS3viaLocalApi(s3FullPath,s3Direct=s3Direct)
        return pd.read_csv(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While reading csv file from S3: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def saveDftoS3(df, s3FullPath,**kwargs):
    """
    Saves csv file in S3

    :param df: Dataframe to save to S3

    :param s3FullPath: S3 path to save the csv

    :param kwargs: arguments to save csv

    :return:
    """
    try:
        s3util = S3Util.S3LocalUtility()
        bucketName, s3filePath = parseS3filePath(s3FullPath)
        localFileLocation = s3util.s3Config.s3_local_folder_path + s3filePath
        makeDirectories(localFileLocation)
        df.to_csv(localFileLocation,**kwargs)
        s3util.uploadFileToS3(localFileLocation, s3filePath, bucketName)
    except Exception as e:
        msg = "Exception While saving dataframe to csv file and uploading to S3: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def readPickleFromS3(s3FullPath,s3Direct=True,**kwargs):
    """
    Read pickle file from S3

    :param s3FullPath: S3 path to read pickle from

    :param s3Direct: if True always downloads from S3, else searches in local and returns if found

    :param kwargs: arguments to save S3

    :return: deserialized pickle object
    """
    try:
        localFileLocation = fetchFileFromS3viaLocalApi(s3FullPath,s3Direct=s3Direct)
        return joblib.load(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While reading pickle file from S3: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)


def checkIfS3FileExist(s3FullPath):
    """
    Check if S3 file exist or not

    :param s3FullPath: S3 file path

    :return: True/False
    """
    s3util = S3Util.S3LocalUtility()
    bucketName, s3filePath = parseS3filePath(s3FullPath)
    return s3util.ifS3FileExist(s3filePath,bucketName)

def getValFromDict(name, data):
    """
    Get the value from the key from a given dictionary and return custom exception messages if not found

    :param name: key to search

    :param data: Dictionary to search from

    :return: value for the given search key
    """
    if name in data and data[name] is not None:
        return data[name]
    elif name not in data:
        raise KeyError(str(name)+" is not defined in the request parameter")
    elif data[name] is None:
        raise TypeError(str(name)+" cannot be None type")

def loadDataFramesFromDict(fileDict):
    """
    Load the dataframes from a given dictionary of file paths

    :param fileDict: {key: 'filepath'}

    :return:{key: file}
    """
    try:
        dfs={}
        for key in fileDict.keys():
            dfs[key]= pd.read_csv(fileDict[key])
        return dfs
    except Exception as e:
        msg ="Unable to load csv file(s) into dataframes: " + str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception()


def loadDataFramesFromList(filePaths):
    """
    Load Dataframes from list

    :param filePaths: list of file paths

    :return: list of files
    """
    try:
        dfs = []
        for i in filePaths:
            df = pd.read_csv(i)
            dfs.append(df)
        return dfs
    except Exception as e:
        msg="Unable to load csv file(s) into dataframes: "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)


def moduleClassFunctionInvoke(moduleClassFunctionPath, *arguments):
    """
    Return a function call dynamically from a string function path.
    It applies reflections to load the function from the given class and module from a string

    :param moduleClassFunctionPath: full path of the module-class-function

    :param arguments: arguments to pass to the function

    :return: function invocation with arguments
    """
    try:
        extractPath=moduleClassFunctionPath.rsplit('.', 2)
        module_name,py_class_name,function_name=extractPath[0],extractPath[1],extractPath[2]
        module = importlib.import_module(module_name)
        py_class = getattr(module, py_class_name)()
        return getattr(py_class, function_name)(*arguments)
    except Exception as e:
        msg="Problem in invocation function: "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)


def moduleClassType(moduleClassFunctionPath):
    """
    Returns the type of a function dynamically from a string function path.

    :param moduleClassFunctionPath: full path of the module-class-function

    :return: type of the invoked function
    """
    try:
        extractPath=moduleClassFunctionPath.rsplit('.', 2)
        module_name,py_class_name,function_name=extractPath[0],extractPath[1],extractPath[2]
        module = importlib.import_module(module_name)
        py_class = getattr(module, py_class_name)()
        return type(py_class)
    except Exception as e:
        msg="Problem in invocation function (Class checking failed):  "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)