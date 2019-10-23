import common_utils.ServiceHelper as util
import traceback
import warnings
from ml_automation.core.contexts import ModelGeneratorContext
warnings.filterwarnings('ignore')
def ModelGenerator(raw_request):
    """
    Action: Perform model generation functions for the given objects

    :param raw_request: request objects to perform model generation on training data

    :return: Status of each object
    """
    output_json = {}
    try:
        preprocessed_df = util.loadDataFramesFromList([util.getValFromDict('preprocessed_file_path', raw_request)])[0]
        model_generators = util.getValFromDict('model_generators_object_list', raw_request)
        modelGeneratorContext=ModelGeneratorContext()
        for model_generator in model_generators:
            try:
                model_id = util.getValFromDict("model_id", model_generator)
                model_shortname = util.getValFromDict("model_shortname", model_generator)
                model_function = util.getValFromDict("python_function", model_generator)
                model_target_file_path = util.getValFromDict("target_model_file_path", model_generator)
                additional_params= util.getValFromDict("additional_params", model_generator)
                util.moduleClassFunctionInvoke(model_function, preprocessed_df, str(model_target_file_path), additional_params, modelGeneratorContext)
                output_json[str(model_id) + ":" + str(model_shortname)] = {'status': 'Success','message': 'Model Successfully Saved'}
            except Exception as e:
                output_json[str(model_id) + ":" + str(model_shortname)] = {'status': 'Failure','message':  str(__name__)+" "+str(type(e).__name__) + ' ' + str(e)+str(traceback.format_exc())}
                continue
    except Exception as e:
        output_json["Exception"] = __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())
    return output_json

