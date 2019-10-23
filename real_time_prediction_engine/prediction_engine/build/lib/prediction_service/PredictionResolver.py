import pandas as pd
from common_utils.MLLogger import MLLogging
import configurations
import prediction_service.constants
from prediction_service.deserializer_predictor.KerasDeserializerPredictor import \
    KerasDeserializerPredictor
from prediction_service.deserializer_predictor.DefaultDeserializerPredictor import \
    DefaultDeserializerPredictor
from common_utils import ServiceHelper

logger=MLLogging.getLog()

def predictorFactory(implementation, dataFrame, pipelineFilename, requestArguments):
    """
    Resolve the Class based on the implementation and perform predictions on them
    and return the predictionContext object containing predictions as response

    :param implementation: Type of the algorithm implementation

    :param dataFrame: Dataframe of features

    :param pipelineFilename: Name of the file to deserialize

    :param requestArguments: Additional arguments

    :return: prediction context object
    """
    try:
        if implementation.lower() == 'keras':
            DeserializerPredictor = KerasDeserializerPredictor()
        else:
            DeserializerPredictor = DefaultDeserializerPredictor()
        predictionContext = DeserializerPredictor.performPredictions(dataFrame, pipelineFilename, requestArguments)
        return predictionContext
    except Exception as e:
        msg="Failed to do predictions in Predictor Factory: "+str(type(e).__name__)+" "+str(e)
        logger.error(msg)
        raise Exception(msg)

def resolve(data):
    """
    This method resolves the data based on the request parameters and returns response containing predictions in desired format

    1.Parse Request Data

    2.Resolve Deserialization and Prediction Class

    3.Prepare the output Dictionary for response

    :param data: Request Data json to be parsed and resolved

    :return: dict_pred: Dictionary of response after resolving request
    """
    try:
        dict_pred = {}
        implementation= ServiceHelper.getValFromDict(prediction_service.constants.Constants.IMPLEMENTATION, data)
        payload = ServiceHelper.getValFromDict(prediction_service.constants.Constants.PAYLOAD, data)
        pipelineFilename = ServiceHelper.getValFromDict(prediction_service.constants.Constants.PIPELINE_FILE_NAME, data)
        requestArguments = ServiceHelper.getValFromDict(prediction_service.constants.Constants.REQUEST_ARGUMENTS, data) if prediction_service.constants.Constants.REQUEST_ARGUMENTS in data  else None
        logger.debug("Request arguments:" +str(requestArguments))
        dataFrame = pd.DataFrame(payload)
        logger.info("Length of payload: " + str(len(dataFrame)))
        predictionContext=predictorFactory(implementation=implementation, dataFrame=dataFrame, pipelineFilename=pipelineFilename, requestArguments=requestArguments)
        if hasattr(predictionContext, 'predictionLabels') and  predictionContext.predictionLabels is not None:
            dict_pred[prediction_service.constants.Constants.PREDICTIONS] = predictionContext.predictionLabels
        if hasattr(predictionContext, 'predictionProbabilities') and predictionContext.predictionProbabilities is not None and predictionContext.classes is not None:
            dict_pred[prediction_service.constants.Constants.PREDICTIONS_PROBABILITIES] = predictionContext.predictionProbabilities
            dict_pred[prediction_service.constants.Constants.CLASSES]=predictionContext.classes
        if hasattr(predictionContext, 'responseArguments') and predictionContext.responseArguments is not None and bool(predictionContext.responseArguments):
            dict_pred[prediction_service.constants.Constants.RESPONSE_ARGUMENTS] = predictionContext.responseArguments
        return dict_pred
    except TypeError as e:
        msg="API Request has None type values: "+str(type(e).__name__)+" "+str(e)
        logger.error(msg)
        raise Exception(msg)
    except KeyError as e:
        msg="All relevant keys must be present in API request. Missing key: "+str(type(e).__name__)+" "+str(e)
        logger.error(msg)
        raise Exception(msg)
    except Exception as e:
        msg="Unable to resolve in Prediction Resolver: "+str(type(e).__name__)+" "+str(e)
        logger.error(msg)
        raise Exception(msg)



