import os,sys
os.chdir("../")
sys.path.insert(0, os.path.join(os.getcwd()))
import common_utils.ServiceHelper as ServiceHelper

def test_parseS3filePath():
    """TESTCASE 1"""
    bucket,filePath=ServiceHelper.parseS3filePath("/s3-bucket/folder/subfolder/file")
    assert (bucket,filePath) == ('s3-bucket','folder/subfolder/file')
    #TESTCASE 2
    bucket, filePath = ServiceHelper.parseS3filePath("s3-bucket/folder/subfolder/file")
    assert (bucket, filePath) == ('s3-bucket', 'folder/subfolder/file')
    #TESTCASE 3
    bucket, filePath = ServiceHelper.parseS3filePath("s-bucket/folder/subfolder/file")
    assert (bucket, filePath) == (None, 's-bucket/folder/subfolder/file')
    ##TESTCASE 4
    bucket, filePath = ServiceHelper.parseS3filePath("")
    assert (bucket, filePath) == (None, '')