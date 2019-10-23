#!flask/bin/python
from prediction_service.constants import Constants
import traceback
import flask
from common_utils.MLLogger import MLLogging
from prediction_service import PredictionResolver
from common_utils.ConfigurationSetups import getEnv
from flask import url_for
from flask import Flask
from worker import celery
import celery.states as states
from flask import request
import json
app = Flask(__name__)
logger=MLLogging.getLog()

@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

@app.route('/mlAutomation', methods=['POST'])
def processRequest():
    raw_request = request.json
    task = celery.send_task('tasks.ml_automation', args=[raw_request], kwargs={})
    response = task.id
    return response

@app.route('/asyncInvocation', methods=['POST'])
def processasyncInvocation():
    raw_request = request.json
    task = celery.send_task('tasks.predictPipeline', args=[raw_request], kwargs={})
    response = task.id
    return response

@app.route('/ping', methods=['GET'])
def ping():
    """Health check for the webservice
    :return: (200,OK) if the server is running
    """
    health = True
    status = 200 if health else 404
    return flask.Response(response='Ok', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def get_prediction():
    """
    Prediction Inference Engine Endpoint. Expects POST arguments containing payload and model artifacts as JSON
    :return: (200,predictions in Json format) else return (202,"Exception message") in case of error
    """
    global logger
    try:
        data = request.json
        logger.info(type(data))
        logger.info("Request received")
        logger.debug("Request Json:: "+str(data))
        dict_pred= PredictionResolver.resolve(data)
        dict_pred=json.dumps(dict_pred)
        logger.debug("Response Json:: " + str(dict_pred))
        logger.info("Returning predictions")
    except Exception as e:
        msg="Failed to perform predictions::"+str(e)
        logger.error(msg)
        logger.error("TRACEBACK DETAILS:: "+str(traceback.format_exc()))
        response=msg+" TRACEBACK:: "+ str(traceback.format_exc())
        return flask.Response(response=response, status=202, mimetype='text')
    finally:
        pass
    return flask.Response(response=dict_pred, status=200, mimetype='application/json')

if __name__ == '__main__':
    try:
        host='0.0.0.0' if getEnv(Constants.HOST) is None else getEnv(Constants.HOST)
        port = '8080' if getEnv(Constants.PORT) is None else getEnv(Constants.PORT)
        app.run(port=int(port), host=host, threaded=True)
    except Exception:
        logger.info("Exception occurred while starting the server: " + str(traceback.format_exc()))

