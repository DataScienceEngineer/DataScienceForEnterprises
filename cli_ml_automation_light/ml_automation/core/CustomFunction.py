import common_utils.ServiceHelper as util
import traceback
import warnings
warnings.filterwarnings('ignore')
def CustomFunction(raw_request):
    """
    Action: Perform a custom function

    :param raw_request: request object to perform custom function with arguments

    :return: Status of the object
    """
    output_json = {}
    try:
        custom_function_object = util.getValFromDict('custom_function_object', raw_request)
        custom_function_id = util.getValFromDict("request_id", custom_function_object)
        custom_function_shortname = util.getValFromDict("request_shortname", custom_function_object)
        custom_function_arguments = util.getValFromDict("arguments", custom_function_object)
        custom_function_path = util.getValFromDict("python_function", custom_function_object)
        try:
            response = util.moduleClassFunctionInvoke(custom_function_path, custom_function_arguments)
            output_json[str(custom_function_id) + ":" + str(custom_function_shortname)]={'status': 'Success', 'message': str(response)}
        except Exception as e:
            output_json[str(custom_function_id) + ":" + str(custom_function_shortname)]={'status': 'Failure', 'message': __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())}
    except Exception as e:
        output_json["Exception"] =  __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())
    return output_json

