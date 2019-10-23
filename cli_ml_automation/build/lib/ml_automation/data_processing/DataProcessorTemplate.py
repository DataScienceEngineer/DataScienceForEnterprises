from abc import ABC,abstractmethod
import pandas as pd
from typing import List,Dict
from ml_automation.core.contexts import DataProcessorContext
class PreprocessingTemplate(ABC):
    @abstractmethod
    def performPreprocessing(self,merged_df:pd.DataFrame, additional_params:Dict, data_processor_context:DataProcessorContext)->pd.DataFrame:
        """
        Perform Preprocessing

        :param merged_df: Contains merged dataframe which is to be preprocessed

        :param additional_params: Contains Additional arguments

        :param data_processor_context: Context variable to be passed across functions for a single call

        :return: preprocessed dataframe
        """
        pass

class MergingTemplate(ABC):
    @abstractmethod
    def performMerging(self,raw_dfs:Dict[str,pd.DataFrame], additional_params:Dict, data_processor_context:DataProcessorContext)->pd.DataFrame:
        """
        Perform Preprocessing

        :param raw_dfs: Contains raws Dataframes which are to be merged

        :param additional_params: Contains Additional arguments

        :param data_processor_context: Context variable to be passed across functions for a single call

        :return: merged dataframe
        """
        pass



