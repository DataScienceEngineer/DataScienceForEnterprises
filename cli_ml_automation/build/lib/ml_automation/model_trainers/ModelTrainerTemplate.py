from abc import ABC,abstractmethod
from typing import Dict
import pandas as pd
from ml_automation.core.contexts import ModelGeneratorContext
class ModeltrainerTemplate(ABC):
    @abstractmethod
    def performModelTraining(self,preprocessed_df:pd.DataFrame,model_target_file_path:str,additional_params:Dict,model_generator_context:ModelGeneratorContext):
        """

        :param preprocessed_df: preprocessed dataframe for training

        :param model_target_file_path: File path for saving the model

        :param additional_params: Dictionary containing additional parameters

        :param model_generator_context: Global Context variable accesible across functions

        :return: Returns status If model is saved or not
        """
        pass

