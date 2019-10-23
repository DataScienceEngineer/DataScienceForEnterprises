import keras
import tensorflow as tf

import common_utils.ConfigurationSetups
from prediction_service.constants import Constants
from common_utils.MLLogger import MLLogging
from threading import Lock
import prediction_service.constants
from prediction_service.deserializer_predictor.context.PipelinePredictionContext import PipelinePredictionContext,PredictionContextError
from common_utils import S3Util, ServiceHelper
import configurations
import numpy as np
s3Config= S3Util.S3Configuration()
logger=MLLogging.getLog()

class KerasDeserializerPredictor(PipelinePredictionContext):
    """
    Keras Algorithms Deserializer and Predictor
    """
    def __init__(self):
        self.dataFrame=None
    def performPredictions(self,dataFrame,pipelineFilename,requestArguments):
        """
        Perform predictions for all Keras based algorithms. This deserializer predictor requires thread and process lock to predict due to tensorflow sessions.

        :param dataFrame: Dataframe to perform predictions on

        :param pipelineFilename: Name of the serialized model pipeline filename to deserialize and predict.

        :param requestArguments: Additional Arguments to consider that was send on request. Like to extract leaf_numbers from trees.

        :return: Prediction Context object containing predictions, probabilities and other prediction related things
        """
        try:
            keras.backend.clear_session()
            self.dataFrame = dataFrame
            predContext = PipelinePredictionContext()
            predContext.pipeLineFileName = pipelineFilename
            predContext.modelFileName = ServiceHelper.getValFromDict(
                prediction_service.constants.Constants.MODEL_FILE_NAME, requestArguments)
            ServiceHelper.fetchFileFromS3viaLocalApi(predContext.pipeLineFileName)
            ServiceHelper.fetchFileFromS3viaLocalApi(predContext.modelFileName)
            predContext.pipeline_load()
            logger.debug("Wait")
            with Lock():
                logger.debug("Acquired Lock")
                session = keras.backend.get_session()
                graph = tf.get_default_graph()
                with session.as_default():
                        with graph.as_default():
                            predContext.loadedPipeLine.named_steps[Constants.PIPELINE_NAMED_STEP_MODEL].model = ServiceHelper.load_h5_file(predContext.modelFileName)
                            predContext.pipeline_predictLabels(dataFrame)
                            try:
                                predContext.pipeline_probabilityDistribution(dataFrame)
                            except PredictionContextError as e:
                                logger.warning("Could not fetch the probability distribution and/or classes due to: " + str(type(e).__name__) + " " + str(e))
                                pass
                            if len(np.shape(predContext.predictionLabels)) == 2:
                                predContext.predictionLabels = np.array(predContext.predictionLabels).flatten().tolist()
                tf.reset_default_graph()
                keras.backend.clear_session()
                logger.debug("Caching pipeline: " + str(ServiceHelper.load_pipeline_cache.cache_info()))
                return predContext
        except KeyError as e:
            msg = "Missing key in the model file. Please check the input features or modify the file. Prediction failed due to: " + str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
        except ValueError as e:
            msg = "Null/NAN/infinity or incompatible data. Prediction failed due to: " + str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
        except Exception as e:
            msg = "Failed to deserialize or Predict Keras Based Models: " +str(type(e).__name__)+" "+str(e)
            logger.error(msg)
            raise Exception(msg)
        finally:
            tf.reset_default_graph()
            keras.backend.clear_session()
            logger.debug("Released Lock")

