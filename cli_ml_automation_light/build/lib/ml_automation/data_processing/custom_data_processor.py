from ml_automation.data_processing.DataProcessorTemplate import PreprocessingTemplate,MergingTemplate
import pandas as pd
from typing import Dict,List
from ml_automation.core.contexts import DataProcessorContext
class DummyPreprocessingTemplate(PreprocessingTemplate):
    """
    Implementation example of Preprocessing by extending PreprocessingTemplate
    """
    def performPreprocessing(self,merged_df:pd.DataFrame, additional_params:Dict, data_processor_context:DataProcessorContext)->pd.DataFrame:
        return merged_df



class TestPreprocessingTemplate1(PreprocessingTemplate):
    """
    Implementation example of Preprocessing by extending PreprocessingTemplate
    """
    def performPreprocessing(self,merged_df:pd.DataFrame, additional_params:Dict, data_processor_context:DataProcessorContext)->pd.DataFrame:
        return merged_df

class DummyMergingTemplate(MergingTemplate):
    """
    Implementation example of Merging by extending MergingTemplate
    """
    def performMerging(self,raw_dfs:Dict[str,pd.DataFrame], additional_params:Dict, data_processor_context:DataProcessorContext)->pd.DataFrame:
        merged_df=raw_dfs['1']
        return merged_df
