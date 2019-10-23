import configparser
import os

def getEnv(env):
    """
    Fetch the value of the OS environment variable

    :param env: OS environment key

    :return: OS environment value
    """
    if env in os.environ.keys() and  os.environ[env] is not None:
        return os.environ[env]
    else: return None

class Singleton(type):
    """
    Singleton Class. Extend this class to make a class a Singleton
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CredentialsConfigurations(metaclass=Singleton):
    """
    Load the secret keys from the credentials file and store the configurations in this class object
    """
    def __init__(self,config_folder,credentials_properties_filename):
        """
        Constructor to initialize Credential configurations parsed from the credential file

        :param config_folder: configuration folder path

        :param credentials_properties_filename: credentials properties file name
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_folder + '/' + credentials_properties_filename)

class ProjectConfigurations(metaclass=Singleton):
    """
    Load the project configurations in this class object
    """
    def __init__(self,vm_env,config_folder,project_properties_filename):
        """
        Constructor to initialize project configurations which is environment specific(dev/testing/prod etc)

        :param vm_env: OS Environment(dev/testing/prod etc)

        :param config_folder: configuration folder path

        :param project_properties_filename: project properties file name
        """
        self.config = configparser.ConfigParser()
        if getEnv(vm_env) is None:
            self.config.read(config_folder + 'local' + '/' + project_properties_filename)
        else:
            self.config.read(config_folder + getEnv(vm_env) + '/' + project_properties_filename)