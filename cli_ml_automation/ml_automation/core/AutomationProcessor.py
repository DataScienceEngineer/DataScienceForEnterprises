import ast
import sys
import traceback
import warnings
import os
warnings.filterwarnings('ignore')
def processFactory(raw_request):
    """
    Resolve the automation object from the raw_request dictionary

    :param raw_request: input dictionary

    :return: resolved request objects
    """
    if "model_generators_object_list" in raw_request:
        from ml_automation.core.ModelGenerator import ModelGenerator
        return ModelGenerator(raw_request)
    elif "model_predictors_object_list" in raw_request:
        from ml_automation.core.ModelPredictor import ModelPredictor
        return ModelPredictor(raw_request)
    elif "data_processing_object_list" in raw_request:
        from ml_automation.core.DataProcessor import DataProcessor
        return DataProcessor(raw_request)
    elif "custom_function_object" in raw_request:
        from ml_automation.core.CustomFunction import CustomFunction
        return CustomFunction(raw_request)
    else:
        raise Exception("No Framework found for automation. Check Parameters.")

if __name__ == "__main__":
    raw_request=None
    output_json={}
    try:
        if len(sys.argv) != 3:
            raise Exception("Requires three arguments. File path. Project Folder. Request Params. Got " + str(len(sys.argv)))
        sys.path.insert(0, sys.argv[1])
        os.chdir(sys.argv[1])
        try:
            raw_request = ast.literal_eval(sys.argv[2])
        except Exception as e:
            raise Exception("Invalid Json or Parameters: " + str(type(e).__name__) + str(e))
        output_json=processFactory(raw_request)
        print(str(output_json))
    except Exception as e:
        output_json["Exception"] =  __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())
        print(output_json)

