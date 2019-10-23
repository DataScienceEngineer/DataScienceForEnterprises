import common_utils.ServiceHelper as util
import traceback
import warnings
from ml_automation.core.contexts import ModelPredictorContext
warnings.filterwarnings('ignore')
def ModelPredictor(raw_request):
    """
    Action: Perform model prediction functions for the given objects

    :param raw_request: request objects to perform model predictions on testing data

    :return: Status of each object
    """
    output_json = {}
    try:
        preprocessed_df = util.loadDataFramesFromList([util.getValFromDict('preprocessed_file_path', raw_request)])[0]
        model_preditors = util.getValFromDict('model_predictors_object_list', raw_request)
        modelPredictorContext=ModelPredictorContext()
        for model_predictor in model_preditors:
            try:
                task_id= util.getValFromDict("task_id", model_predictor)
                task_shortname = util.getValFromDict("task_shortname", model_predictor)
                additional_params = util.getValFromDict("additional_params", model_predictor)
                model_function = util.getValFromDict("python_function", model_predictor)
                model_file_paths = util.getValFromDict("model_file_paths", model_predictor)
                prediction_file_path= util.getValFromDict("target_file_path", model_predictor)
                pred_df= util.moduleClassFunctionInvoke(model_function, model_file_paths, preprocessed_df, additional_params, modelPredictorContext)
                pred_df.to_csv(prediction_file_path, index=False)
                output_json[str(task_id) + ":" + str(task_shortname)] = {'status': 'Success','message': 'Predictions Successfully Saved'}
            except Exception as e:
                output_json[str(task_id) + ":" + str(task_shortname)] = {'status': 'Failure','message': str(__name__)+" "+str(type(e).__name__) + ' ' + str(e)+str(traceback.format_exc())}
                continue
    except Exception as e:
        output_json["Exception"] =  __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())
    return output_json
