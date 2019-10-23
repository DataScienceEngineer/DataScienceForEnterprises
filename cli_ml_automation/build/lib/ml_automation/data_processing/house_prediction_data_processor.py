from ml_automation.data_processing.DataProcessorTemplate import PreprocessingTemplate
from typing import Dict
from ml_automation.core.contexts import DataProcessorContext
from ml_automation.housing_price_prediction.core_functions import *
class HousePredictionDataProcessor(PreprocessingTemplate):
    """
    Implementation example of Preprocessing by extending PreprocessingTemplate
    """
    def performPreprocessing(self,merged_df:pd.DataFrame, data_processor_context:Dict, merged_df_processor_context:DataProcessorContext)->pd.DataFrame:
        merged_df[data_processor_context['catvars']] = feature_enggCatvars(data_processor_context['catvars'],
                                                         merged_df[data_processor_context['catvarspredictor']],
                                                         data_processor_context['json_files']['categorical_frequency_labels'],
                                                         data_processor_context['json_files']['ordinal_labels'],
                                                         predictor_var=data_processor_context['predictor_var'],
                                                         type=data_processor_context['type'])
        merged_df[data_processor_context['temporalvarspredictor']] = feature_enggTemporalvars(merged_df[data_processor_context['temporalvarspredictor']],
                                                                            data_processor_context['temporalvars'],
                                                                            data_processor_context['basevar'])
        merged_df[data_processor_context['extravar']] = feature_enggExtrafeature(merged_df[data_processor_context['extra_new_var']])
        merged_df[data_processor_context['numvars']] = feature_enggNumvars(merged_df[data_processor_context['numvars']],
                                                         data_processor_context['numvars'], data_processor_context['json_files']['mean_values'],
                                                         type=data_processor_context['type'])
        merged_df[data_processor_context['skewedvars']] = feature_enggSkewedvars(merged_df[data_processor_context['skewedvars']],
                                                               data_processor_context['skewedvars'])
        return merged_df
