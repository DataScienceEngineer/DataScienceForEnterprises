from common_utils.MLLogger import MLLogging
import configurations
import boto3
import botocore
logger=MLLogging.getLog()

class S3Configuration(object):
    """Initialize S3 Configuration Object from the project properties file"""
    def __init__(self):
        config = configurations.projectConfigurations.config
        credentialsConfig= configurations.credentialsConfiguration.config
        self.s3_local_folder_path= config['S3']['S3_local_folder_path']
        if 'AWS Credentials' in credentialsConfig.keys():
            if 'access_key' in credentialsConfig['AWS Credentials'].keys() and credentialsConfig['AWS Credentials']['access_key'] is not None:
                self.access_key = credentialsConfig['AWS Credentials']['access_key']
            if 'secret_key' in credentialsConfig['AWS Credentials'].keys() and credentialsConfig['AWS Credentials']['secret_key'] is not None:
                self.secret_key = credentialsConfig['AWS Credentials']['secret_key']
        if 'default_bucket_name' in config['S3'].keys() and config['S3']['default_bucket_name'] is not None: self.default_bucket_name = config['S3']['default_bucket_name']


class S3LocalUtility():
    """S3 Local Utility"""
    def __init__(self,bucket=None):
        """
        Construct S3Utility based on the region and the default bucket

        :param region: S3 Region

        :param bucket: S3 Bucket
        """
        self.s3Config=S3Configuration()
        if bucket is not None: self.s3Config.default_bucket_name = bucket
        self.s3_client = boto3.client('s3',aws_access_key_id=self.s3Config.access_key,aws_secret_access_key=self.s3Config.secret_key)
        self.s3_session = boto3.Session(aws_access_key_id=self.s3Config.access_key, aws_secret_access_key=self.s3Config.secret_key)
    def downloadFileFromS3(self, s3fileLocation,localFileLocation, bucket=None):
        """
        Download file from S3 given the bucket name and S3 relative Path. After Downloading it will create the relative directories

        :param s3fileLocation: S3 relative path

        :param bucket: S3 bucket name

        :return: None
        """
        try:
            print(localFileLocation)
            logger.debug("Downloading file from S3 ... " + s3fileLocation)
            if bucket is None:
                self.s3_client.download_file(self.s3Config.default_bucket_name, s3fileLocation, localFileLocation)
            else:
                self.s3_client.download_file(bucket, s3fileLocation, localFileLocation)
        except Exception as e:
            msg="Exception While downloading from S3"+ str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)

    def uploadFileToS3(self,fileName,key,bucket=None):
        """
        Upload file to S3

        :param fileName: file to upload

        :param key: S3 upload file location

        :param bucket: bucket where the file is to be uploaded

        :return:
        """
        try:
            logger.debug("Uploading file to S3 ... " + fileName)
            if bucket is None:
                self.s3_client.upload_file(fileName, self.s3Config.default_bucket_name, key,ExtraArgs={'ServerSideEncryption': 'AES256'})
            else:
                self.s3_client.upload_file(fileName, bucket, key,ExtraArgs={'ServerSideEncryption': 'AES256'})
        except Exception as e:
            msg = "Exception While uploading to S3" + str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)

    def ifS3FileExist(self,key,bucket=None):
        """
        Check if S3 file exists or not

        :param key: S3 file key to check

        :param bucket: S3 bucket where the S3 file key resides

        :return: True/False
        """
        try:
            logger.info("Checking file if it exists :: "+" key: "+str(key)+" bucket: "+str(bucket))
            s3 = self.s3_session.resource('s3')
            if bucket is None:
                s3.Object(self.s3Config.default_bucket_name, key).load()
            else:
                s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise Exception(str(e))
        return True


