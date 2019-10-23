import logging
from logging.handlers import TimedRotatingFileHandler

import common_utils.ConfigurationSetups

import common_utils.constants
import configurations
import os


class LoggingConfig():
    """Retrieve the Logger Configurations from the project properties"""
    def __init__(self):
        config = configurations.projectConfigurations.config
        self.loggerName=config['Logs']['logger_default_name']
        self.logFilePath = config['Logs']['log_file_path']
        self.logFilePrefix = str(config['Logs']['log_file_prefix']+'-id-'+self.getUniqueId()+'.log')
        self.logFormatterString='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        self.logTimeRotator=config['Logs']['log_time_rotator']
        self.logTimeInterval=int(config['Logs']['log_time_interval'])
        self.logFileHandlerLevel=self.__logMapper(config['Logs']['log_level_file'])
        self.logStreamHandlerLevel = self.__logMapper(config['Logs']['log_level_console'])
        self.logType =config['Logs']['logger_type']

    def getUniqueId(self):
        """
        Get the container Id from docker runtime. If not running on Docker get the process id

        :return: unique Id for logger name
        """
        if common_utils.constants.Constants.CONTAINER_ID not in os.environ.keys() or os.environ[
            common_utils.constants.Constants.CONTAINER_ID] is None:
            return str(os.getpid())
        else:
            return str(os.environ[common_utils.constants.Constants.CONTAINER_ID]) + '_' + str(os.getpid())

    def __logMapper(self, logLevel_str):
        """
        Set different logging level according to the given string

        :param logLevel_str: Given String for logging levl

        :return: logging level
        """
        if logLevel_str.upper() == "CRITICAL" or logLevel_str.upper() == "FATAL":
            return logging.CRITICAL
        elif logLevel_str.upper() == "ERROR":
            return logging.ERROR
        elif logLevel_str.upper() == "WARNING" or logLevel_str.upper() == "WARN":
            return logging.WARNING
        elif logLevel_str.upper() == "INFO":
            return logging.INFO
        elif logLevel_str.upper() == "DEBUG":
            return logging.DEBUG
        else:
            return logging.NOTSET

class MLLogging(metaclass=common_utils.ConfigurationSetups.Singleton):
    """A Singleton Class to initialize Logger which is to be used the project modules"""
    def __init__(self):
        """
        Initialize Logging Module with all the given configurations for this environment
        """
        MLLogging.loggerConfig = LoggingConfig()
        MLLogging.logger = initloggerConfiguration(logConfig=MLLogging.loggerConfig)

    def getLog(name=None):
        """
        Returns the logger that was created

        :return: return the created logger object
        """
        return MLLogging.logger

def initloggerConfiguration(logConfig=None):
    """
    Initialize a logger object from the configuration properties

    :param logConfig: logger configurations

    :return: logger object
    """
    logger = logging.getLogger(logConfig.loggerName)
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(logConfig.logFilePath):
        os.makedirs(logConfig.logFilePath)
    if logConfig.logType == "TimedRotatingFileHandler":
        fh = logging.handlers.TimedRotatingFileHandler(logConfig.logFilePath + logConfig.logFilePrefix,when=logConfig.logTimeRotator,interval=logConfig.logTimeInterval)
    else:
        fh = logging.FileHandler(logConfig.logFilePath + logConfig.logFilePrefix)
    fh.setLevel(logConfig.logFileHandlerLevel)
    ch = logging.StreamHandler()
    ch.setLevel(logConfig.logStreamHandlerLevel)
    formatter = logging.Formatter(logConfig.logFormatterString)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


MLLogging()
