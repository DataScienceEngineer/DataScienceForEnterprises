import common_utils.ServiceHelper as util
from ml_automation.data_processing.DataProcessorTemplate import MergingTemplate,PreprocessingTemplate
import traceback
import warnings
from ml_automation.core.contexts import DataProcessorContext
warnings.filterwarnings('ignore')
def DataProcessor(raw_request):
    """
    Action: Perform Merging, then Preprocessing for the given objects

    :param raw_request: request objects to perform merging and pre-processing of data

    :return: status of each object
    """
    output_json = {}
    try:
        raw_dfs = util.loadDataFramesFromDict(
            util.getValFromDict('raw_file_paths', raw_request))
        processed_data_file_path = util.getValFromDict('processed_data_file_path', raw_request)
        data_processing_objects = util.getValFromDict('data_processing_object_list', raw_request)
        data_processor_context=DataProcessorContext()
        preprocessed_df=None
        for data_processor in data_processing_objects:
            try:
                data_process_id= util.getValFromDict("data_process_id", data_processor)
                data_process_shortname = util.getValFromDict("data_process_shortname", data_processor)
                additional_params = util.getValFromDict("additional_params", data_processor)
                data_processing_function = util.getValFromDict("python_function", data_processor)
                if preprocessed_df is None:
                    if len(raw_dfs.keys())>1 and not issubclass(
                            util.moduleClassType(data_processing_function), MergingTemplate):
                        raise NotImplementedError("Multiple raw files found, but Merging function was not implemented")
                    elif len(raw_dfs.keys())==1 and issubclass(
                            util.moduleClassType(data_processing_function), MergingTemplate):
                        raise NotImplementedError("Expected Multiple raw files for Merging")
                    elif len(raw_dfs.keys())==1 and  issubclass(
                            util.moduleClassType(data_processing_function), PreprocessingTemplate):
                        #Make preprocessed_df=raw_dfs
                        preprocessed_df=[raw_dfs[raw_df] for raw_df in raw_dfs.keys()][0]
                        preprocessed_df = util.moduleClassFunctionInvoke(data_processing_function, preprocessed_df, additional_params, data_processor_context)
                        output_json[str(data_process_id) + ":" + str(data_process_shortname)] = {'status': 'Success','message': 'Preprocessing Completed'}
                    else:
                        preprocessed_df = util.moduleClassFunctionInvoke(data_processing_function, raw_dfs, additional_params, data_processor_context)
                        output_json[str(data_process_id) + ":" + str(data_process_shortname)] = {'status': 'Success','message': 'Merging Completed'}


                else:
                    preprocessed_df = util.moduleClassFunctionInvoke(data_processing_function, preprocessed_df, additional_params, data_processor_context)
                    output_json[str(data_process_id) + ":" + str(data_process_shortname)] = {'status': 'Success','message': 'Preprocessing Completed'}
            except Exception as e:
                output_json[str(data_process_id) + ":" + str(data_process_shortname)] = {'status': 'Failure','message': str(__name__)+" "+str(type(e).__name__) + " " + str(e)+str(traceback.format_exc())}
                break
        try:
            preprocessed_df.to_csv(processed_data_file_path)
        except:
            raise Exception("Failed to save the processed dataframe into csv, due to invalid dataframe format")
    except Exception as e:
        output_json["Exception"] =  __name__+" "+str(type(e).__name__)+" "+ str(e)+str(traceback.format_exc())
    return output_json
