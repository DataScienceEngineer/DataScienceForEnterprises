from ml_automation.data_processing.DataProcessorTemplate import PreprocessingTemplate
from typing import Dict
from ml_automation.core.contexts import DataProcessorContext
from ml_automation.housing_price_prediction.core_functions import *
class HousePredictionDataProcessor(PreprocessingTemplate):
    """
    Implementation example of Preprocessing by extending PreprocessingTemplate
    """
    def performPreprocessing(self, merged_df:pd.DataFrame, additional_params:Dict, merged_df_processor_context:DataProcessorContext)->pd.DataFrame:
        merged_df[additional_params['catvars']] = feature_enggCatvars(additional_params['catvars'],
                                                                      merged_df[additional_params['catvarspredictor']],
                                                                      additional_params['json_files']['categorical_frequency_labels'],
                                                                      additional_params['json_files']['ordinal_labels'],
                                                                      predictor_var=additional_params['predictor_var'],
                                                                      type=additional_params['type'])
        merged_df[additional_params['temporalvarspredictor']] = feature_enggTemporalvars(merged_df[additional_params['temporalvarspredictor']],
                                                                                         additional_params['temporalvars'],
                                                                                         additional_params['basevar'])
        merged_df[additional_params['extravar']] = feature_enggExtrafeature(merged_df[additional_params['extra_new_var']])
        merged_df[additional_params['numvars']] = feature_enggNumvars(merged_df[additional_params['numvars']],
                                                                      additional_params['numvars'], additional_params['json_files']['mean_values'],
                                                                      type=additional_params['type'])
        merged_df[additional_params['skewedvars']] = feature_enggSkewedvars(merged_df[additional_params['skewedvars']],
                                                                            additional_params['skewedvars'])
        return merged_df
