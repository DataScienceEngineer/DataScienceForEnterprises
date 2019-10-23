import time
from worker import celery
import random
from ml_automation.core.AutomationProcessor import processFactory
from common_utils.MLLogger import MLLogging
from prediction_service import PredictionResolver
import traceback
logger=MLLogging.getLog()

@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(30)
    return x + y


@celery.task(name='tasks.ml_automation')
def ml_automation(raw_request):
    output_json=processFactory(raw_request)
    return output_json

@celery.task(name='tasks.predictPipeline')
def predictPipeline(request):
    global logger
    try:
        data = request
        logger.info(type(data))
        logger.info("Request received")
        logger.debug("Request Json:: "+str(data))
        dict_pred= PredictionResolver.resolve(data)
        logger.debug("Response Json:: " + str(dict_pred))
        logger.info("Returning predictions")
        return dict_pred
    except Exception as e:
        msg="Failed to perform predictions::"+str(e)
        logger.error(msg)
        logger.error("TRACEBACK DETAILS:: "+str(traceback.format_exc()))
        response=msg+" TRACEBACK:: "+ str(traceback.format_exc())
        return response
    finally:
        pass
    return response
