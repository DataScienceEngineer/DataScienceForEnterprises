from prediction_service.deserializer_predictor.context.PipelinePredictionContext import PipelinePredictionContext,PredictionContextError
from common_utils import ServiceHelper
from common_utils.MLLogger import MLLogging
from prediction_service.constants import Constants
import numpy as np
logger=MLLogging.getLog()
class DefaultDeserializerPredictor(PipelinePredictionContext):
    """
    Scikit learn Algorithms Deserializer and Predictor
    """
    def __init__(self):
        self.dataFrame=None

    def performPredictions(self,dataFrame,pipelineFilename,requestArguments):
        """
        Perform predictions for all Scikit-learn algorithms and all Custom Algorithm implemented with Scikit-Learn pipelines

        :param dataFrame: Dataframe to perform predictions on

        :param pipelineFilename: Name of the serialized model pipeline filename to deserialize and predict.

        :param requestArguments: Additional Arguments to consider that was send on request. Like to extract leaf_numbers from trees.

        :return: Prediction Context object containing predictions, probabilities and other prediction related things
        """
        try:
            self.dataFrame = dataFrame
            predContext = PipelinePredictionContext()
            predContext.responseArguments = {}
            predContext.pipeLineFileName = pipelineFilename
            ServiceHelper.fetchFileFromS3viaLocalApi(predContext.pipeLineFileName)
            predContext.pipeline_load()
            predContext.pipeline_predictLabels(dataFrame)
            try:
                predContext.pipeline_probabilityDistribution(dataFrame)
            except PredictionContextError as e:
                logger.warning("Could not fetch the probability distribution and/or classes due to: "+str(type(e).__name__)+" "+str(e))
                pass
            if requestArguments is not None and Constants.IS_LEAF_NUMBER in requestArguments and requestArguments[Constants.IS_LEAF_NUMBER].lower()=="true":
                predContext.getLeafNumber(dataFrame)
                predContext.responseArguments[Constants.LEAF_NUMBER]= [[i] for i in predContext.leafNumber] if len(np.shape(predContext.leafNumber)) == 1 else predContext.leafNumber
            logger.debug("Caching: " + str(ServiceHelper.load_pipeline_cache.cache_info()))
            return predContext
        except KeyError as e:
            msg="Missing key in the model file. Please check the input features or modify the file. Prediction failed due to: "+str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
        except ValueError as e:
            msg="Null/NAN/infinity or incompatible data. Prediction failed due to: "+str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
        except Exception as e:
            msg="Failed to deserialize or Predict Default Pipeline Based Models: "+str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
