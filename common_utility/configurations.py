from common_utils.ConfigurationSetups import CredentialsConfigurations, ProjectConfigurations


class Constants:
    IMPLEMENTATION= 'implementation'
    PAYLOAD= 'payload'
    PIPELINE_FILE_NAME= 'pipelineFilename'
    MODEL_FILE_NAME= 'modelFilename'
    PREDICTIONS= 'predictions'
    PREDICTIONS_PROBABILITIES='predictions_prob'
    REMOTE_S3_ERROR_CODE='Failed to process the request !!!'
    VM_ENVIRONMENT_VARIABLE= 'DEPLOY_ENV'
    CONFIGURATION_FOLDER='configs/'
    PROJECT_PROPERTIES_FILENAME = 'project.properties'
    CREDENTIALS_PROPERTIES_FILENAME='credentials.properties'
    LEAF_NUMBER='leaf_number'
    IS_LEAF_NUMBER = 'isLeafNumber'
    CONTAINER_ID='HOSTNAME'
    CLASSES='classes'
    PIPELINE_NAMED_STEP_MODEL='model'
    PIPELINE_NAMED_STEP_MAPPER='mapper'
    REQUEST_ARGUMENTS='requestArguments'
    RESPONSE_ARGUMENTS='responseArguments'
    HOST='HOST'
    PORT='PORT'


projectConfigurations= ProjectConfigurations(Constants.VM_ENVIRONMENT_VARIABLE, Constants.CONFIGURATION_FOLDER, Constants.PROJECT_PROPERTIES_FILENAME)
credentialsConfiguration= CredentialsConfigurations(Constants.CONFIGURATION_FOLDER, Constants.CREDENTIALS_PROPERTIES_FILENAME)
