from abc import ABC,abstractmethod
from typing import Dict
import pandas as pd
from ml_automation.core.contexts import ModelPredictorContext
class ModelPredictorTemplate(ABC):
    @abstractmethod
    def performModelPredictions(self,model_file_paths:Dict,preprocessed_df:pd.DataFrame,additional_params:Dict,model_predictor_context:ModelPredictorContext)->pd.DataFrame:
        """

        :param model_file_paths: Dictionary of file paths of models for this tasks

        :param preprocessed_df: Preprocessed Dataframe to be used in model predictions

        :param additional_params: Dictionary of additional arguments

        :param model_predictor_context: Global Context variable accesible across functions

        :return: Prediction Dataframes
        """
        pass


